# Flask Authentication Application

This is a simple Flask application that implements user authentication with registration, login, and logout functionalities. It includes features like password hashing, session management, and form validation.

## Features

- **User Registration:** Users can create a new account with a unique username and password.
- **User Login:** Registered users can log in with their credentials.
- **Protected Dashboard:** Only authenticated users can access the dashboard.
- **User Logout:** Users can log out from their account.

## Technologies Used

- **Flask:** Python web framework for developing the application.
- **Flask-SQLAlchemy:** ORM for managing database operations.
- **Flask-Login:** Session management for handling user authentication.
- **Flask-Bcrypt:** Password hashing for securing user passwords.
- **Flask-WTF:** Form handling and validation.

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/flask-auth-app.git
    cd flask-auth-app
    ```

Set up the SQLite database:

    ```bash
    python
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    ```

### Running the Application

1. Start the Flask development server:

    ```bash
    python app.py
    ```

2. Open your web browser and go to:

    ```
    http://127.0.0.1:5000/
    ```



### Routes

- **`/`** - Home page, renders `index.html`.
- **`/login`** - Login page, renders `login.html` and handles login logic.
- **`/signup`** - Signup page, renders `signup.html` and handles user registration.
- **`/dashboard`** - Protected dashboard page, accessible only to logged-in users.
- **`/logout`** - Logout route, logs the user out and redirects to the login page.

### Forms

- **`RegisterForm`** - Handles user registration with validation for username and password.
- **`LoginForm`** - Handles user login with validation for username and password.

### Database Model

- **`User`** - A model representing a user in the database, with fields for `id`, `username`, and `password`.

### Security

- **Password Hashing:** Passwords are hashed using Flask-Bcrypt before being stored in the database.
- **Session Management:** User sessions are managed using Flask-Login, ensuring only authenticated users can access certain routes.
