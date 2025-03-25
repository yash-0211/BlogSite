import datetime
import json 
import os
import jwt
from werkzeug.security import  check_password_hash
from flask import request , session
from core import app
from core.apis import api
from core.decorator import token_required
from core.apis.user import UserResource, ProfilePicResource
from core.apis.feed import FeedResource
from core.apis.blog import BlogResource
from core.apis.follower import FollowResource
from core.apis.comment import CommentResource , CommentListResource 
from core.apis.like import LikeResource
from core.models.user import User
from core.models.blog import Blog
from core.models.follower import Follower


api.add_resource(UserResource, '/users/<string:name>' )
api.add_resource(BlogResource,  '/post/<string:postid>' )
api.add_resource(CommentResource,  '/comment/<int:id>' )
api.add_resource(CommentListResource,  '/commentlist/<string:postid>' )
api.add_resource(LikeResource,  '/like/<string:postid>' )
api.add_resource(FeedResource,  '/home' )
api.add_resource(ProfilePicResource,  '/profile_pic' )
api.add_resource(FollowResource,  '/follow/<string:other_user>' )

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
    u_obj= User.get(username)
    
    if u_obj is not None and check_password_hash(u_obj.password, password):
        session['logged_in']= True
        token= jwt.encode(
        payload= { 'username': username, 'id': u_obj.get_id(),
            'expiration': str(datetime.datetime.now()+ datetime.timedelta(seconds=120)) }
            , key= app.config['SECRET_KEY'])
        return {"access_token":token }
    return {}


@app.route('/search', methods=["POST"])
def search():
    data = json.loads(request.data)
    name = data.get("username", None)
    users= User.search(name)
    print("SEARCH FOR: ", name, users)
    names= []
    for u in users:
        names.append(u.username)
    return {"names": names}


@app.route('/myaccount', methods=["GET"])
@token_required
def myaccount(token):
    userid = token['id']
    followers= Follower.get_followers(userid)
    followings= Follower.get_followings(userid)
    posts= Blog.get_posts(userid)
    dict= {"posts":[p.id for p in posts[-1::-1]], "followers":followers, "followings":followings, "userid":userid, "err":""}
    dict["ispic"]= os.path.exists(f"core/static/img/propics/{userid}.jpg")
    return dict

if __name__ == '__main__':
    app.run(port=5000, debug=True)
