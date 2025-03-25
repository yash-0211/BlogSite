from functools import wraps
from flask import request, session, jsonify
import jwt
from core import app

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token= request.headers.get('Authentication-Token') 
        if not token or token=="null":
            session['logged_in']= False
            return jsonify( {'Alert':'Token missing'} )
        try:
            payload= jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except:
            session['logged_in']= False
            return jsonify( {'Alert':'Incorrect token'} )
        return func( payload,*args, **kwargs )  
    return decorated

