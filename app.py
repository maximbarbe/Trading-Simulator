from flask import Flask, render_template, redirect, request
from forms import registerForm
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from config import Config
from models import User, Trade

# Initialisation of a user
user = None

# Give admin privileges
admin = False

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)
csrf = CSRFProtect(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Base route when someone joins the server
@app.route("/")
def index():

    return render_template("index.html", user = user)


# Register route, will handle register form.
@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = registerForm(request.form)
    if request.method == "POST" and register_form.validate():
        if (register_form.check_email_equal(register_form.email.data, register_form.confirm_email.data) and
            register_form.check_name_length(register_form.name.data) and register_form.check_email_length(register_form.email.data) and
            register_form.check_password_length(register_form.password.data) and register_form.check_valid_email(register_form.email.data) and
            register_form.check_valid_password(register_form.password.data)):
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


