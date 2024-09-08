from flask import Flask,render_template,url_for,redirect,jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import InputRequired,Length, ValidationError
from flask_migrate import Migrate

app=Flask(__name__)
bcrypt=Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///test.db"
app.config["SECRET_KEY"]='thisisasecretkey'


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


db=SQLAlchemy(app)
migrate=Migrate(app,db,render_as_batch=True)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    password=db.Column(db.String(50),nullable=False)
   

class Bond(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(80))
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(80),nullable=False)
    date_posted=db.Column(db.DateTime,default=datetime.now)
    tags=db.Column(db.String(200),nullable=False)
    

class Comments(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    commentID=db.Column(db.Integer)
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(80),nullable=False)
    date_posted=db.Column(db.DateTime,default=datetime.now)

class Like(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    likeID=db.Column(db.Integer)
    author=db.Column(db.String(80),nullable=False)
    date_posted=db.Column(db.DateTime,default=datetime.now)

class Doctors(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50),nullable=False,unique=True)
    name=db.Column(db.String(50),nullable=False)
    qualifications=db.Column(db.String(50),nullable=False)
    specialties=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(50),nullable=False)

    
    
  




class RegisterForm(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Username"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})
    submit=SubmitField("Submit")
    def validate_username(form,username):
        existing_user=User.query.filter_by(username=username.data).first()

        if existing_user:
            flash("This usernamealready exists",'info')
            raise ValidationError("This username already exists")
    

class Login(FlaskForm):
    username=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'username'})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'Password'})

    submit=SubmitField('Submit')

class Bond_page(FlaskForm):
    title=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={'placeholder':'Enter Title'})
    content=TextAreaField("Your views matter a lot",render_kw={'placeholder':'Share your views'})
    submit=SubmitField("Post your views")
    tags=StringField(validators=[InputRequired(),Length(min=4,max=200)],render_kw={'placeholder':'Tags'})

class CommentForm(FlaskForm):
    comment=TextAreaField(render_kw={'placeholder':'Comment here'})
    submit=SubmitField('Post')

class LikeForm(FlaskForm):
    submit=SubmitField('Like')

class DoctorDetails(FlaskForm):
    email=StringField(validators=[InputRequired(),Length(min=4,max=50)],render_kw={"placeholder":"Email"})
    name=StringField(validators=[InputRequired(),Length(min=4,max=100)],render_kw={"placeholder":"Name"})
    qualifications=StringField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Degrees"})
    specialties=StringField(validators=[InputRequired(),Length(min=4,max=100)],render_kw={"placeholder":"Specialties"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})
    
    submit=SubmitField("Submit")
    def validate_username(form,email):
        existing_doctor=Doctors.query.filter_by(email=email.data).first()

        if existing_doctor:
            flash("This usernamealready exists",'info')
            raise ValidationError("This username already exists")
     
class doctor_login(FlaskForm):
    email=StringField(validators=[InputRequired(),Length(min=4,max=50)],render_kw={"placeholder":"Email"})
    password=PasswordField(validators=[InputRequired(),Length(min=4,max=20)],render_kw={"placeholder":"Password"})
    submit=SubmitField("Submit")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form=Login()
    if form.validate_on_submit():
        user_in=User.query.filter_by(username=form.username.data).first()
        if user_in:
            if bcrypt.check_password_hash(user_in.password,form.password.data):
                login_user(user_in)
                return redirect('/dashboard')
                
           
    
    return render_template('login.html',form=form)

@app.route('/signup',methods=['GET','POST'])
def signup():
    form=RegisterForm()
    

    if form.validate_on_submit():
        hashed_pass=bcrypt.generate_password_hash(form.password.data)
        new_user=User(username=form.username.data,password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
        


    return render_template('signup.html',form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    user_logged=current_user
    return render_template('dashboard.html',user_logged=user_logged)

@app.route('/bond',methods=['POST','GET'])
@login_required
def bonding():
    
    posts=Bond.query.order_by(Bond.date_posted.desc()).all()
    return render_template("bonding.html",posts=posts)

@app.route('/delete/<int:id>',methods=['GET','POST'])
@login_required
def delete_post(id):
    post=Bond.query.get_or_404(id)
    if post.author==current_user.username:
        try:
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('bonding'))
        except:
            return("You cant delete this post")
        
    else:
        return redirect('/dashboard')
   
        
@app.route('/write',methods=['GET','POST'])
@login_required
def write():
    form=Bond_page()
    

    if form.validate_on_submit():
        post=Bond(content=form.content.data,author=current_user.username,title=form.title.data,tags=form.tags.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('bonding'))
    

    posts = Bond.query.filter_by(author=current_user.username).order_by(Bond.date_posted.desc()).all()
    
    return render_template('write.html',form=form,posts=posts)

@app.route('/comment/<int:id>',methods=['GET','POST'])
@login_required
def comment(id):
    post_comment=Bond.query.get_or_404(id)
    form=CommentForm()
    if form.validate_on_submit():
        user_comment=Comments(content=form.comment.data,author=current_user.username,commentID=post_comment.id)
        db.session.add(user_comment)
        db.session.commit()
        return redirect(url_for('bonding'))
    comments=Comments.query.filter_by(commentID=post_comment.id).order_by(Comments.date_posted.desc()).all()
    comments_count=Comments.query.filter_by(commentID=post_comment.id).count()
    return render_template('comment.html',post_comment=post_comment,comments=comments,form=form,comments_count=comments_count)

@app.route('/delete_comment/<int:id>')
@login_required
def delete_comment(id):
    comment_to_delete=Comments.query.get_or_404(id)
    if comment_to_delete.author==current_user.username:
        try:
            db.session.delete(comment_to_delete)
            db.session.commit()
            return redirect(url_for('bonding'))
        except:
            return("You cant delete this post")
        
    else:
        return redirect('/write')
    
@app.route('/like/<int:id>',methods=['GET','POST'])
@login_required
def like_post(id):
    liked_post=Bond.query.get_or_404(id)
    form=LikeForm()
    if form.validate_on_submit():
        # Check if the user already liked this post
        like = Like.query.filter_by(author=current_user.username, likeID=liked_post.id).first()
        if like:
            
            db.session.delete(like)
            db.session.commit()
            flash('You unliked this post.', 'success')
            return redirect(url_for('bonding'))
        else:
            
            new_like = Like(author=current_user.username, likeID=liked_post.id)
            db.session.add(new_like)
            db.session.commit()
            flash('You liked this post!', 'success')

        #try:
            #like=Like(likeID=liked_post.id,author=current_user.username)
            #db.session.add(like)
            #db.session.commit()
            #return redirect(url_for('bonding'))
        #except:
            return redirect(url_for('bonding'))
    like_count=Like.query.filter_by(likeID=liked_post.id).count()
    return render_template('like.html',form=form,like_count=like_count,liked_post=liked_post)

@app.route('/doctor',methods=['GET','POST'])
def doctor():
    form=DoctorDetails()
    if form.validate_on_submit():
        hashed_doctor_pass=bcrypt.generate_password_hash(form.password.data)
        new_doc=Doctors(password=hashed_doctor_pass,name=form.name.data,email=form.email.data, qualifications=form.qualifications.data,specialties=form.specialties.data)
        db.session.add(new_doc)
        db.session.commit()
        return redirect('/doc_login')
    return render_template('doctor_signup.html',form=form)

@app.route('/doc_login',methods=['GET','POST'])
def doc_login():
    form=doctor_login()
    if form.validate_on_submit():
        doctor_in=Doctors.query.filter_by(email=form.email.data).first()
        if doctor_in:
            if bcrypt.check_password_hash(doctor_in.password,form.password.data):
                login_user(doctor_in)
                return redirect('/doc_page')

    return render_template('doctor_login',form=form)

@app.route('/doc_page',methods=['GET','POST'])
@login_required
def doctor_page():
    doc_logged=current_user
    return render_template('doc_page.html',doc_logged=doc_logged)

@app.route('/doc_list',methods=['GET','POST'])
@login_required
def doc_list():
    res_doctors=Doctors.query.all()
    return render_template('doc_list.html',res_doctors=res_doctors)

@app.route('/doc_details/<int:id>',methods=['GET','POST'])
@login_required
def consult(id):
    doc_to_book=Doctors.query.get_or_404(id)
    return render_template('doc_details.html',doc_to_book=doc_to_book)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect ('/login')


if __name__=='__main__':
    app.run(debug=True)


