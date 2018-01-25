from functools import wraps
from flask import redirect, url_for, session


def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session.keys():
            return redirect(url_for('sign_up_screen'))
        return function(*args, **kwargs)
    return decorated_function
