from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

character_message = "is required to be between 1 and 100 character."

class userForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired(), Length(1, 100, f"Name {character_message}")], description="Name")
    email = EmailField(label="Email", validators=[DataRequired(), Length(1, 100, f"Email {character_message}")], description="Email")
    confirm_email = EmailField(label="Email", validators=[DataRequired(), Length(1, 100, f"Email {character_message}"), EqualTo("name", "Must be equal to the email field.")], description="Confirm email")
    password = PasswordField(label="Password", validators=[DataRequired(), Length(1, 100, f"Password {character_message}")], description="Password")
    submit = SubmitField(label="Submit")