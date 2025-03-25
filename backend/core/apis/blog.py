from flask import request, session
from core.decorator import token_required
from flask_restful import  Resource 
from core import app, cache
import jwt
import os
from core.models.user import User
from core.models.blog import Blog
from core.models.like import Like


class BlogResource(Resource):

    @cache.memoize(10)
    def get(self, postid):
        token= request.headers.get('Authentication-Token')
        if token == "null":
            token = None
        if token:
            session['logged_in']= False
            try: token= jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            except: token= None
        
        post_obj = Blog.query.filter_by(id=postid).first()
        likes = Like.get_likes(postid)
        islike = token['id'] in likes
        userid = post_obj.author
        username = User.get_by_id(userid).username
        obj= { "author":username, "title":post_obj.title, "caption":post_obj.caption, 
            "ispic": os.path.isfile("static/img/propics/"+ str(userid)+ ".jpg"),
            "datetime":post_obj.datetime, "islike":islike, "likes":len(likes) , 'userid': userid }
        return obj

    @token_required
    def put(token, self, postid):
        filename= ""
        try:
            last_post = Blog.query.order_by(Blog.id.desc()).first()
            filename = str(last_post.id + 1)
        except:
            filename= "1"

        file = request.files.get("file" )
        title = request.form.get("title")
        content = request.form.get("content") 

        if file:
            p= "core/static/img/posts/"+ filename+".jpg"
            file.save(os.path.join(p))
        userid = token['id']
        Blog.upload(userid,filename,content,title)
        return {}

    @token_required
    def post(token, self, postid):
        file = request.files.get("file" )
        title = request.form.get("title")
        caption = request.form.get("caption")

        post_= Blog.get(postid)
        if post_ is None or post_[0] != token['id']:
            return {}
        p= "core/static/img/posts/"+ postid+".jpg"
        if file:
            file.save(os.path.join(p))
        else:
            try: os.remove(p)
            except: pass
        Blog.edit(postid, title, caption)
        print("POST EDITED !!")
        return {}

    @token_required
    def delete(token, self, postid):
        result = Blog.delete(postid, token['id'])
        path = "core/static/img/posts/"+ postid+".jpg"
        if os.path.exists(path):
            os.remove(path)
        if result: 
            pass
        return {}
