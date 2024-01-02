from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import Config
from forms import userForm
from models import User
from database import db
from routes import routes

# Initialisation of a user
user = None

# Give admin privileges
admin = False


# App configuration
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(routes)

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


