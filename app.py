from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import Config
from forms import userForm
from models import User
from database import db


# Initialisation of a user
user = None

# Give admin privileges
admin = False


# App configuration
app = Flask(__name__)
app.config.from_object(Config)


# Setup login manager
login_manager = LoginManager(app)

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Configuration for csrf protection
csrf = CSRFProtect(app)



# with app.app_context():
#     db.create_all()

# Base route when someone joins the server
@app.route("/")
def index():

    return render_template("index.html", user = user)


# Register route, will handle register form.
@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = userForm(request.form)
    if request.method == "POST" and register_form.validate():
        return redirect("/")
    return render_template("register.html", form=register_form)
    

    

# Login route, will add the user to the session and redirect to base directory
@app.route("/login", methods=["GET", "POST"])
def login():
    return "<b>Login Page</b>"

# Logout route, will remove the user from the session and redirect to base directory
@app.route("/logout")
def logout():
    
    return redirect("/")
