from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_cors import CORS
from config import Config
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_caching import Cache


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.app_context().push()

db=SQLAlchemy()
db.init_app(app)
cache = Cache(app)


class user(db.Model, UserMixin):
    __tablename__= "user"
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String,nullable=False,unique=True)
    email= db.Column(db.String,nullable=True)
    password=db.Column(db.String,nullable=False)

    def create(name, email, password): # create_user_dao
        u_obj = user(username=name, password=generate_password_hash(password), email=email)
        db.session.add(u_obj)
        db.session.commit()
        return u_obj

    def get(name): # get_user
        return user.query.filter_by(username=name).first()
    
    def get_by_email(email): # get_user_by_email
        return user.query.filter_by(email=email).first()
    
    def alreadyExist(name,email):
        e = user.query.filter_by(email=email).first()
        u = user.query.filter_by(username=name).first()
        if u: return "username"
        if e: return "email"
        return None
    
    def update_name(username, newname):  # change_data
        posts = post.query.filter_by(author=username).all()
        for p in posts:
            p.author= newname
        comments = comment.query.filter_by(author=username).all()
        for c in comments:
            c.author= newname
        likes = like.query.filter_by(author=username).all()
        for l in likes:
            l.author= newname
        followings = follower.query.filter_by(person=username).all()
        for f in followings:
            f.person= newname
        followers = follower.query.filter_by(following=username).all()
        for f in followers:
            f.following= newname
        db.session.commit()
    
    def delete(username):
        post.query.filter_by(author=username).delete() 
        comment.query.filter_by(author=username).delete()
        like.query.filter_by(author=username).delete()
        follower.query.filter_by(person=username).delete()
        follower.query.filter_by(following=username).delete()
        user.query.filter_by(username=username).delete()
        db.session.commit()
    
    def search(name): # search_dao
        return user.query.filter(user.username.startswith(name)).all()


class post(db.Model):
    __tablename__= "post"
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    author= db.Column(db.String,db.ForeignKey('user.username'),nullable=False)
    title= db.Column(db.String,nullable=False)
    caption= db.Column(db.String)
    datetime= db.Column(db.String,nullable=False)
    image = db.Column(db.String)

    # @cache.memoize(10)
    def get(postid): # get_post
        post_obj = post.query.filter_by(id=postid).first()
        if post_obj is None: 
            return None
        return post_obj.author , post_obj.title , post_obj.caption

    def upload(username,filename,content,title): # upload_post
        p = post(author=username, image=filename, caption=content, datetime=str(datetime.datetime.now())[:-10], title=title)
        db.session.add(p)
        db.session.commit()

    def edit(postid,title,caption): # edit_post
        post_obj = post.query.filter_by(id=postid).first()
        post_obj.title=title
        post_obj.caption=caption
        post_obj.datetime=str(datetime.datetime.now())[:-10]
        db.session.commit()
    
    def delete(postid, username): # delete_post
        post_obj = post.query.filter_by(id=postid).first()
        if post_obj and (post_obj.author == username):
            comment.query.filter_by(postid =postid).delete()
            like.query.filter_by(postid =postid).delete()
            post.query.filter_by(id=postid).delete()
            db.session.delete(post_obj)
            db.session.commit()
            return True
        return False

    def get_posts(name):
        return post.query.filter_by(author=name).all()

    @cache.memoize(10)
    def get_home_posts(username): # home
        print("Getting home posts from models.py")
        f_obj= follower.query.filter_by(person=username).all()
        follows = [f.following for f in f_obj]
        follows.append(username)
        posts= db.session.query(post).filter(post.author.in_(follows))
        return list(posts)



class follower(db.Model):
    # The "person" follows "following". Means person is follower of "following"
    __tablename__= "follower"
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    person= db.Column(db.String,db.ForeignKey("user.username"), nullable=False)
    following= db.Column(db.String, db.ForeignKey("user.username"), nullable=False)
    datetime= db.Column(db.String,nullable=False)

    def follow(person, other): # follow_dao
        f_obj= follower.query.filter_by(person=person,following= other).first()
        if not f_obj:
            f_obj= follower(person=person, following=other, datetime=str(datetime.datetime.now())[:-10])
            db.session.add(f_obj)
            db.session.commit()

    def unfollow(person, other):
        f_obj = follower.query.filter_by(person=person,following=other).first()
        db.session.delete(f_obj)
        db.session.commit()
    
    # @cache.memoize(10)
    def get_followers(name):
        followers= follower.query.filter_by(following=name).all()
        followers= [obj.person for obj in followers]
        return followers

    @cache.memoize(10)
    def get_followings(name):
        followings = follower.query.filter_by(person=name).all()
        followings= [obj.following for obj in followings]
        return followings


class comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String,db.ForeignKey("user.username"), nullable=False)
    postid = db.Column(db.Integer,db.ForeignKey("post.id"), nullable=False)
    caption = db.Column(db.String, nullable=False)
    datetime= db.Column(db.String,nullable=False)

    def add(username, postid, caption): # add_Comment
        c = comment(author=username, postid=postid, caption=caption, datetime=str(datetime.datetime.now())[:-10])
        db.session.add(c)
        db.session.commit()
        comm = comment.query.order_by(comment.id.desc()).first()
        return comm.id
    
    def delete(id): # delete_Comment
        c = comment.query.filter_by(id=id).first()
        db.session.delete(c)
        db.session.commit()
    
    def get_list(postid): # get_Comments
        return comment.query.filter_by(postid=postid).all()


class like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String,db.ForeignKey("user.username"), nullable=False)
    postid = db.Column(db.Integer,db.ForeignKey("post.id"), nullable=False)

    def add(author, postid):
        l = like(author=author, postid =postid)
        db.session.add(l)
        db.session.commit()
    def delete(author, postid):
        islike =like.query.filter_by(postid =postid, author=author).first()
        if islike:
            db.session.delete(islike)
            db.session.commit()


db.create_all()
print("MODELS CREATED !! ", user, post, like, comment, follower)
