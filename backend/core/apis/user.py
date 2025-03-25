from core.schedule_email import send_mail
from flask import request, session, redirect
from flask_restful import  Resource 
from werkzeug.security import generate_password_hash, check_password_hash
import json
import jwt
import os
import datetime
from core import app, cache, db
from core.decorator import token_required
from core.models.user import User
from core.models.blog import Blog
from core.models.comment import Comment
from core.models.follower import Follower


class UserResource(Resource):

    def put(self, name= None):
        data = json.loads(request.data)
        username = data.get("username", None)
        email_id = data.get("email", None)
        password = data.get("password", None)
        if " " in username:
            return {"message": " Whitespace is not allowed in username" }
        print("DATA RECEIVED: ", username, email_id, password)
        message= User.alreadyExist(username,email_id)
        if message:
            return {"message":message}
        
        user = User.create(username, email_id, password)
        
        session['logged_in']= True
        token= jwt.encode(
            payload= { 'username': username, 'id': user.get_id(),
            'expiration': str(datetime.datetime.now()+ datetime.timedelta(seconds=120)) }
            , key= app.config['SECRET_KEY'])
        welcomeMsg= "Hello! Welcome to the BlogSite app. We hope you will enjoy using the app"
        send_mail(receiver=email_id ,message=welcomeMsg, subject= "Welcome !!" )
        return {"access_token":token, "message":""}

    @cache.memoize(10)
    def get(self, name):
        print("Get user : ", name)
        user_obj = User.get(name)
        if not user_obj:
            return {'error': 'User not found'}
        followers= Follower.get_followers(name)
        followings= Follower.get_followings(name)
        posts = Blog.get_posts(user_obj.id)
        dict= {"posts":[p.id for p in posts], "followers":followers, "followings":followings, "userid":user_obj.id, "err":""}
        dict["ispic"] =  os.path.exists(f"core/static/img/propics/{user_obj.id}.jpg")
        return dict
    
    @token_required
    def post(token, self, name):
        data = json.loads(request.data)
        msg = data.get("message", None)
        password = data.get("password", None)
        username= token['username']
        u_obj = User.get(username)
        if not check_password_hash(u_obj.password, password):
            return {"err":True}
        
        if msg=="EditUsername":
            newname = data.get("newname", None)
            if User.get(newname):
                return {"username_already_exist":True}
            u_obj.username= newname
            db.session.commit()
            User.update_name(username, newname)
            res = app.make_response(redirect("/home"))
            res.set_cookie("username",newname, expires="Mon, 01 Jan 2026 00:00:00 GMT")
            welcomeMsg= "Hello! Your username has been changed!"
            send_mail(receiver=u_obj.email ,message=welcomeMsg, subject= "Username Changed!")

        elif msg=="EditEmail":
            newemail = data.get("email", None)
            if User.get_by_email(newemail):
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
            posts = Blog.query.filter_by(author=username).all()
            sn=1
            for p in posts:
                numComments= len(list(Comment.query.filter_by(postid=p.id).all()))
                f.write(f"{sn},{p.id},{p.datetime},{p.title},{p.caption},{numComments}\n")
                sn += 1
            f.close()
            return {"err": False, "download":True}
        else:
            User.delete(username)
            db.session.delete(u_obj)
            db.session.commit()
        return {"err": False}




class ProfilePicResource(Resource):

    @token_required
    def post(token, self):
        file = request.files.get("file")
        id= token['id']
        p= "core/static/img/propics/"+ str(id) +".jpg"
        file.save(os.path.join(p))
        return {}
    
    @token_required
    def delete(token, self):
        id= token['id']
        try:
            path= "core/static/img/propics/"+ str(id) +".jpg"
            os.remove(path)
            
        except:
            pass
        finally:
            return {}
