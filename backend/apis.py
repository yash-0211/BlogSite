from models import *
from schedule_email import send_mail
from flask import request, session, redirect, jsonify
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
import json 
import jwt
import os
import datetime
import jwt
from functools import wraps

api= Api(app)

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



class User(Resource):

    def put(self, name= None):
        data = json.loads(request.data)
        username = data.get("username", None)
        email_id = data.get("email", None)
        password = data.get("password", None)
        if " " in username:
            return {"message": " Whitespace is not allowed in username" }
        print("DATA RECEIVED: ", username, email_id, password)
        message= user.alreadyExist(username,email_id)
        if message:
            return {"message":message}
        session['logged_in']= True
        token= jwt.encode(
            payload= { 'username': username,
            'expiration': str(datetime.datetime.now()+ datetime.timedelta(seconds=120)) }
            , key= app.config['SECRET_KEY'])
        user.create(username, email_id, password)
        welcomeMsg= "Hello! Welcome to the BlogSite app. We hope you will enjoy using the app"
        send_mail(receiver=email_id ,message=welcomeMsg, subject= "Welcome !!" )
        return {"access_token":token, "message":""}

    @cache.memoize(10)
    def get(self, name):
        print("Get user : ", name)
        e= user.get(name)
        if not e: return {}
        followers= follower.get_followers(name)
        followings= follower.get_followings(name)
        posts= post.get_posts(name)
        dict= {"posts":[p.id for p in posts], "followers":followers, "followings":followings, "userid":e.id, "err":""}
        dict["ispic"]=  os.path.exists(f"static/img/propics/{e.id}.jpg")
        return dict
    
    @token_required
    def post(token, self, name):
        print("EDITPROFILE !!")
        data = json.loads(request.data)
        msg = data.get("message", None)
        password = data.get("password", None)
        username= token['username']
        u_obj=user.get(username)
        if not check_password_hash(u_obj.password, password):
            return {"err":True}
        
        if msg=="EditUsername":
            newname = data.get("newname", None)
            if user.get(newname):
                return {"username_already_exist":True}
            u_obj.username= newname
            db.session.commit()
            user.update_name(username, newname)
            res = app.make_response(redirect("/home"))
            res.set_cookie("username",newname, expires="Mon, 01 Jan 2025 00:00:00 GMT")
            welcomeMsg= "Hello! Your username has been changed!"
            send_mail(receiver=u_obj.email ,message=welcomeMsg, subject= "Username Changed!")

        elif msg=="EditEmail":
            newemail = data.get("email", None)
            if user.get_by_email(newemail):
                return {"email_already_exist":True}
            u_obj.email= newemail
            db.session.commit()
            welcomeMsg= "Hello! Your email has been changed! Kindly contact us if it wasn't you"
            send_mail(receiver=u_obj.email ,message=welcomeMsg, subject= "Email Changed !")

        elif msg=="EditPassword":
            newpassword = data.get("newpassword", None)
            u_obj.password= generate_password_hash(newpassword)

            welcomeMsg= "Hello! Your password has been changed! Kindly contact us if it wasn't you"
            send_mail(receiver=u_obj.email ,message=welcomeMsg, subject= "Password Changed !")
            db.session.commit()

        elif msg=="GetData":
            filepathname= "./static/csvdatafiles/"+ username+".csv"
            f = open(filepathname, 'w')
            header = "Serial No.,id,datetime,title,caption,no. of comments"
            f.write(header + "\n")
            posts = post.query.filter_by(author=username).all()
            sn=1
            for p in posts:
                numComments= len(list(comment.query.filter_by(postid=p.id).all()))
                f.write(f"{sn},{p.id},{p.datetime},{p.title},{p.caption},{numComments}\n")
                sn += 1
            f.close()
            return {"err": False, "download":True}
        else:
            user.delete(username)
            db.session.delete(u_obj)
            db.session.commit()
        return {"err": False}


class Post(Resource):

    @cache.memoize(10)
    def get(self, postid):
        token= request.headers.get('Authentication-Token')
        if token == "null":
            token = None
        if token:
            session['logged_in']= False
            try: token= jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            except: token= None

        post_obj= post.query.filter_by(id=postid).first()
        likes= like.query.filter_by(postid=postid).all()
        likes= [l.author for l in likes]
        islike= token['username'] in likes
        userid = user.get(post_obj.author).id
        obj= { "author":post_obj.author, "title":post_obj.title, 
            "caption":post_obj.caption, "datetime":post_obj.datetime,
            "ispic": os.path.isfile("static/img/propics/"+ str(userid)+ ".jpg"),
            "islike":islike, "likes":len(likes) , 'userid': userid }
        print("ispic= ", obj['ispic'])
        return obj

    @token_required
    def put(token, self, postid):
        print("UPLOAD !!")
        last_post = post.query.order_by(post.id.desc()).first()
        username= token['username']
        filename= ""
        try:
            filename = str(last_post.id + 1)
        except:
            filename= "1"

        file = request.files.get("file" )
        title = request.form.get("title")
        content = request.form.get("content") 

        if file:
            p= "./static/img/posts/"+ filename+".jpg"
            file.save(os.path.join(p))
        post.upload(username,filename,content,title)
        return {}

    @token_required
    def post(token, self, postid):
        file = request.files.get("file" )
        title = request.form.get("title")
        caption = request.form.get("caption")

        post_= post.get(postid)
        if post_ is None or post_[0] != token['username']:
            return {}
        p= "./static/img/posts/"+ postid+".jpg"
        if file:
            # print("Saving the file")
            file.save(os.path.join(p))
        else:
            try: os.remove(p)
            except: pass
        post.edit(postid,title,caption)
        print("POST EDITED !!")
        return {}

    @token_required
    def delete(token, self, postid):
        result = post.delete(postid,token['username'])
        path = "./static/img/posts/"+ postid+".jpg"
        if os.path.exists(path):
            os.remove(path)
        if result: 
            pass
        return {}
        

class Comment(Resource):

    @token_required
    def put(token, self, id):
        data = json.loads(request.data)
        postid = data.get("postid", None)
        username= token['username']
        newComment= data.get("newComment", None)
        print(newComment)
        comm_id= comment.add(username, postid, newComment)
        id= user.query.filter_by(username=username).first().id
        ispic= os.path.exists(f"static/img/propics/{id}.jpg")
        dict={"comment":{ "id":comm_id, "author":username, "caption": newComment, "userid":"", "ispic": False,
                        "userid": id, "ispic": ispic}}
        return dict
    
    @token_required
    def delete(token, self, id):
        comment.delete(id)
        return {}


class CommentList(Resource):

    def get(self, postid):
        comms= comment.get_list(postid)
        dict={"comments":[]}
        for comm in comms:
            id= user.query.filter_by(username=comm.author).first().id
            obj= {"id":comm.id, "author":comm.author, "caption":comm.caption, "userid":id,
                "ispic":os.path.exists(f"static/img/propics/{id}.jpg"),
                }
            dict["comments"].append(obj)
        return dict


class Like(Resource):

    @token_required
    def put(token, self, postid):
        like.add(token['username'], postid)
        return {}
        
    @token_required
    def delete(token, self, postid):
        like.delete(token['username'], postid)
        return {}


class Feed(Resource):

    @token_required
    @cache.memoize(10)
    def get(token, self):
        username = token['username']
        posts= post.get_home_posts(username)
        dict= {}
        posts= posts[-1::-1]
        posts= [post.id for post in posts]
        dict["more"]= len(posts)>5
        dict["posts"]= posts
        print("Getting data from feed !!!")
        return dict
    
    @token_required
    def post(token, self):
        username= token['username']
        data = json.loads(request.data)
        length = data.get("length")
        posts= post.get_home_posts(username)
        posts=  posts[-1::-1]
        if len(posts)< length+5:
            posts=  posts[length-1:length+5]
        else:
            posts= posts[length-1:]
        return {"posts": [post.id for post in posts]}
        

class ProfilePic(Resource):

    @token_required
    def post(token, self):
        file = request.files.get("file")
        id= user.get(token['username']).id
        print("id= ", id)
        p= "./static/img/propics/"+ str(id) +".jpg"
        file.save(os.path.join(p))
        return {}
    
    @token_required
    def delete(token, self):
        id= str(user.get(token['username']).id)
        try:
            p= "./static/img/propics/"+ id +".jpg"
            os.remove(p)
        except:
            pass
        return {}



class Follow(Resource):
    # /follow/

    @token_required
    def post(token, self, other_user): #follow
        person = token['username']
        follower.follow(person, other_user)
        return {}
    
    @token_required
    def delete(token, self, other_user): #unfollow
        person = token['username']
        follower.unfollow(person, other_user)
        return {}

