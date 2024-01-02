from flask import Flask, render_template, url_for, request, redirect, session
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import Config
from markupsafe import escape
from forms import userForm


# Initialisation of a user
user = None

# Give admin privileges
admin = False


# App configuration
app = Flask(__name__)
app.config.from_object(Config)


# Setup login manager
login_manager = LoginManager(app)

# Database configuration
db = SQLAlchemy(app)


# Configuration for csrf protection
csrf = CSRFProtect(app)


# Database model for a single user
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    authenticated = db.Column(db.Boolean, default=False)
    trades = db.relationship('Trade', backref='user')
    

    def is_active(self):
        return True

    def get_id(self):
        return self.id
    
    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
    
    def __repr__(self):
        return f"<User> {self.name}"

# Database model for a single trade
class Trade(db.Model):
    trade_id = db.Column(db.Integer, primary_key = True)
    ticker = db.Column(db.String(10), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    buy_or_sell = db.Column(db.String(10), nullable = False)
    currency = db.Column(db.String(10), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Trade> {'Buy' if self.buy_or_sell == 'buy' else 'Sell'} {self.ticker} at {self.price} {self.currency}"


# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

with app.app_context():
    db.create_all()

# Base route when someone joins the server
@app.route("/")
def index():

    return render_template("index.html", user = user)


# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = userForm(request.form)
    if request.method == "POST" and register_form.validate():
        print("okay")
    return render_template("register.html", form=register_form)
    

    

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    return "<b>Login Page</b>"

# Logout route
@app.route("/logout")
def logout():
    
    return redirect("/")
