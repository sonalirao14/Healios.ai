# Flask Web Application

This project is a Flask-based web application that provides functionalities like user registration, login, creating posts (called "Bonds"), commenting, liking, managing doctors, and more. The application uses SQLite as the database and Flask-WTF for handling forms.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Form Handling](#form-handling)
- [Routes](#routes)
- [Templates](#templates)
- [Contributing](#contributing)
- [License](#license)

## Features

- User registration and login
- Create, read, update, and delete (CRUD) functionality for posts (called "Bonds")
- Comment on posts
- Like and unlike posts
- Doctor registration and login
- Doctor consultation details
- Separate login flows for regular users and doctors

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- Flask-Migrate
- Flask-WTF
- WTForms

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repository.git


Project Structure

your-repository/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── bonding.html
│   ├── write.html
│   ├── comment.html
│   ├── like.html
│   ├── doctor_signup.html
│   ├── doctor_login.html
│   ├── doc_page.html
│   ├── doc_list.html
│   └── doc_details.html
├── static/                 # Static files (CSS, JS, Images)
└── migrations/             # Database migrations
