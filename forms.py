# Forms that will be used in the application

import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError
from flask_bcrypt import check_password_hash
from database import db
from models import User

# Regular expression to check email validity
email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')  

# Regular expression to check password validity
# Password must contain a minimum of 8 characters, at least one letter, one number and and one special character
password_regex = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")

# Form used for the register page
class RegisterForm(FlaskForm):
    name = StringField(label="Name", description="Name")
    email = StringField(label="Email", description="Email")
    confirm_email = StringField(label="confirm_email", description="Confirm email")
    password = PasswordField(label="Password", description="Password")
    submit = SubmitField(label="Submit")
    
    # Use regular expressions to check if email is valid format.
    def check_valid_email(self, email):
        if re.fullmatch(email_regex, email):
            return True
        self.email.errors += (ValidationError("Email format is invalid"),)
        return False

    # Use regular expressions to check if password is valid format.
    def check_valid_password(self, password):
        if re.fullmatch(password_regex, password):
            return True
        self.password.errors += (ValidationError("Password must contain a minimum of 8 characters, at least one letter, one number and one special character."),)
        return False

    # Check if the name entered is correct length.
    def check_name_length(self, name):
        if len(name) < 1 or len(name) > 100:
            self.name.errors += (ValidationError("Name must be between 1 and 100 characters."),)
            return False
        return True

    # Check if email entered is correct length.
    def check_email_length(self, email):
        if len(email) < 6 or len(email) > 100:
            self.email.errors += (ValidationError("Email must be between 6 and 100 characters."),)
            return False
        return True
    
    # Check if both emails entered are equal.
    def check_email_equal(self, email, confirmed_email):
        if email != confirmed_email:
            self.confirm_email.errors += (ValidationError("Emails must be equal."),)
            return False
        return True

    # Check if password is correct length.
    def check_password_length(self, password):
        if len(password) > 100:
            self.password.errors += (ValidationError("Password must be less than 100 characters"),)
            return False
        return True
    
    def check_user_already_exists(self, email):
        user = User.query.filter_by(email=email).first()
        if user != None:
            self.email.errors += (ValidationError("Email already exists."),)
        return True if user != None else False
    
# Form used for the login page
class LoginForm(FlaskForm):
    email = StringField(label="Email", description="Email")
    password = PasswordField(label="Password", description="Password")
    submit = SubmitField(label="Submit")

    # Email verification
    def check_email_exists(self, email):
        user = User.query.filter_by(email=email).first()
        if user == None:
            self.email.errors += (ValidationError("Email does not exist."),)
        return False if user == None else True
    
    def verify_password(self, email, password):
        user = User.query.filter_by(email = email).first()
        if not check_password_hash(user.password, password):
            self.password.errors += (ValidationError("Incorrect password"),)        
            return False
        return True