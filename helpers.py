from flask import redirect, url_for
from flask_login import current_user
from functools import wraps

# Redefine login_required wrapper to redirect user to login page if the user tries to access a locked page
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function