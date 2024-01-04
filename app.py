from flask import Flask, render_template, redirect, request, url_for
from forms import RegisterForm, LoginForm
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt, generate_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from config import Config
from models import User, Trade
from database import db
from helpers import login_required

# Give admin privileges
admin = False

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager(app)
csrf = CSRFProtect(app)
db.init_app(app)
# Setup Bcrypt for storing passwords safely
bcrypt = Bcrypt(app)


# Callback function for getting a user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Base route when someone joins the server
@app.route("/")
def index():
    return render_template("index.html")


# Register route, will handle register form.
@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm(request.form)
    if request.method == "POST" and register_form.validate():
        # All verifications needed to make sure the data is valid
        if (register_form.check_email_equal(register_form.email.data, register_form.confirm_email.data) and
            register_form.check_name_length(register_form.name.data) and register_form.check_email_length(register_form.email.data) and
            register_form.check_password_length(register_form.password.data) and register_form.check_valid_email(register_form.email.data) and
            register_form.check_valid_password(register_form.password.data)) and not register_form.check_user_already_exists(register_form.email.data):
            # Adding a new user to the database
            db.session.add(User(
                name = register_form.name.data,
                email = register_form.email.data,
                password = generate_password_hash(register_form.password.data, 12),
                authenticated = True
            ))     
            db.session.commit()
            return redirect(url_for('login'))       
    return render_template("register.html", form=register_form)
    

    

# Login route, will add the user and redirect to base directory
@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)
    if request.method == "POST" and login_form.validate_on_submit():
        if (login_form.check_email_exists(login_form.email.data) and login_form.verify_password(login_form.email.data, login_form.password.data)):
            user = User.query.filter_by(email=login_form.email.data).first()
            login_user(user)
            return redirect(url_for('index'))
    return render_template("login.html", form=login_form)

# Logout route, will remove the user from the session / log them out and redirect to base directory

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# View trades and profit chart.
@app.route("/trades")
@login_required
def view_trades():
    # Get all trades done by 
    trades = Trade.query.filter_by(user_id = current_user.get_id()).all()
    return render_template("viewTrades.html", trades = trades)