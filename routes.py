from flask import Blueprint, render_template, request, redirect
from models import User
from forms import userForm
from database import db


# Initialisation of a user
user = None

# Give admin privileges
admin = False

routes = Blueprint('routes', __name__, template_folder='templates', static_folder='static')



# Base route when someone joins the server
@routes.route("/")
def index():

    return render_template("index.html", user = user)


# Register route, will handle register form.
@routes.route("/register", methods=["GET", "POST"])
def register():
    register_form = userForm(request.form)
    if request.method == "POST" and register_form.validate():
        return redirect("/")
    return render_template("register.html", form=register_form)
    

    

# Login route, will add the user to the session and redirect to base directory
@routes.route("/login", methods=["GET", "POST"])
def login():
    return "<b>Login Page</b>"

# Logout route, will remove the user from the session and redirect to base directory
@routes.route("/logout")
def logout():
    
    return redirect("/")