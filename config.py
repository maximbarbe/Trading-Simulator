import os
from dotenv import dotenv_values


basedir = os.path.abspath(os.path.dirname(__file__))

# Get secret key from environment variables
env_values = dotenv_values(".env")

class Config:
    SECRET_KEY = env_values['SECRET']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "project.db") 
    SQLALCHEMY_TRACK_MODIFICATIONS = False