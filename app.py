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
migrate=Migrate(app,db)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    password=db.Column(db.String(50),nullable=False)

class Bond(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(80),nullable=False)
    date_posted=db.Column(db.DateTime,default=datetime.now)


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
    
    content=TextAreaField("Your views matter a lot",render_kw={'placeholder':'Share your views'})
    submit=SubmitField("Post your views")

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
        post=Bond(content=form.content.data,author=current_user.username)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('bonding'))
    posts = Bond.query.filter_by(author=current_user.username).order_by(Bond.date_posted.desc()).all()
    return render_template('write.html',form=form,posts=posts)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect ('/login')


if __name__=='__main__':
    app.run(debug=True)


