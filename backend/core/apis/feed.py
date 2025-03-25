from flask_restful import  Resource 
from core.decorator import token_required
from core import cache
import json 
from flask import request

from core.models.blog import Blog

class FeedResource(Resource):

    @token_required
    @cache.memoize(10)
    def get(token, self):
        userid = token['id']
        posts= Blog.get_home_posts(userid)
        dict= {}
        posts= posts[-1::-1]
        posts= [post.id for post in posts]
        dict["more"]= len(posts)>5
        dict["posts"]= posts
        print("Getting data from feed !!!")
        return dict
    
    @token_required
    def post(token, self):
        userid= token['id']
        data = json.loads(request.data)
        length = data.get("length")
        posts= Blog.get_home_posts(userid)
        posts=  posts[-1::-1]
        if len(posts)< length+5:
            posts=  posts[length-1:length+5]
        else:
            posts= posts[length-1:]
        return {"posts": [post.id for post in posts]}
        