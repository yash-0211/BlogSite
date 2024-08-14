import datetime
import json 
import os
import jwt
from werkzeug.security import  check_password_hash
from flask import request , session
from apis import *
from models import *

api.add_resource(User, '/users/<string:name>' )
api.add_resource(Post,  '/post/<string:postid>' )
api.add_resource(Comment,  '/comment/<int:id>' )
api.add_resource(CommentList,  '/commentlist/<string:postid>' )
api.add_resource(Like,  '/like/<string:postid>' )
api.add_resource(Feed,  '/home' )
api.add_resource(ProfilePic,  '/profile_pic' )
api.add_resource(Follow,  '/follow/<string:other_user>' )


@app.route('/nav', methods=["GET"])
@token_required
def nav(token):
    return {"message":"Logged in", "username":token['username'] }


@app.route('/getname', methods=["POST"])
@token_required
def getname(token):
    return {"username": token['username']}


@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    username = data.get("username", None)
    password = data.get("password", None)
    u_obj= user.get(username)
    
    if u_obj is not None and check_password_hash(u_obj.password, password):
        session['logged_in']= True
        token= jwt.encode(
        payload= { 'username': username,
            'expiration': str(datetime.datetime.now()+ datetime.timedelta(seconds=120)) }
            , key= app.config['SECRET_KEY'])
        return {"access_token":token }
    return {}


@app.route('/search', methods=["POST"])
def search():
    data = json.loads(request.data)
    name = data.get("username", None)
    users= user.search(name)
    print("SEARCH FOR: ", name, users)
    names= []
    for u in users:
        names.append(u.username)
    return {"names": names}



@app.route('/myaccount', methods=["GET"])
@token_required
def myaccount(token):
    name= token['username']
    current_user= user.get(name)
    followers= follower.get_followers(name)
    followings= follower.get_followings(name)
    posts= post.get_posts(name)
    dict= {"posts":[p.id for p in posts[-1::-1]], "followers":followers, "followings":followings, "userid":current_user.id, "err":""}
    dict["ispic"]= os.path.exists(f"static/img/propics/{current_user.id}.jpg")
    return dict


if __name__ == '__main__':
    app.run()
