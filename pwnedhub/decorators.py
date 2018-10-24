from flask import g, request, redirect, url_for, abort, make_response
from constants import ROLES
from functools import wraps
from threading import Thread
from urlparse import urlparse

def login_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        parsed_url = urlparse(request.url)
        location = parsed_url.path
        if parsed_url.query:
            location += '?{}'.format(parsed_url.query)
        return redirect(url_for('auth.login', next=location))
    return wrapped

def roles_required(*roles):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if ROLES[g.user.role] not in roles:
                return abort(403)
            return func(*args, **kwargs)
        return wrapped
    return wrapper

def async(func):
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

def no_cache(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        response = make_response(func(*args, **kwargs))
        response.headers['Pragma'] = 'no-cache'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Expires'] = '0'
        return response
    return wrapped
