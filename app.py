from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

from dotenv import dotenv_values
from markupsafe import escape

# Initialisation of a user
user = None
# Get secret key from environment variables
env_values = dotenv_values(".env")

# App configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIOBS'] = False
app.secret_key = env_values['SECRET']
db = SQLAlchemy(app)


# Database model for a single user
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    trades = db.relationship('Trade', backref='user')

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


# with app.app_context():
#     db.create_all()


# Base route when someone joins the server
@app.route("/")
def index():

    return render_template("index.html", user = user)



@app.route("/register")
def register():
    return "<b>Register Page</b>"


@app.route("/login")
def login():
    return "<b>Login Page</b>"

@app.route("/logout")
def logout():

    return redirect("/")
