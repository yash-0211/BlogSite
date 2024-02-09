from models import db, user, post, follower, comment
import datetime
from models import app
from werkzeug.security import generate_password_hash, check_password_hash
from time import perf_counter_ns
from flask_caching import Cache

db.create_all()

cache = Cache(app)

def get_user(name):
    e = user.query.filter_by(username=name).first()
    return e

def get_user_by_email(email):
    e = user.query.filter_by(email=email).first()
    return e

def create_user_dao(name, email, password):
    u_obj = user(username=name, password=generate_password_hash(password, method='sha256'), email=email)
    db.session.add(u_obj)
    db.session.commit()
    return u_obj

def alreadyExist(name,email):
    e = user.query.filter_by(email=email).first()
    u = user.query.filter_by(username=name).first()
    if e is not None:
        return "email"
    if u is not None:
        return "username"
    return None

@cache.memoize(10)
def get_home_posts(username): # home
    f_obj= follower.query.filter_by(person=username).all()
    follows = [f.following for f in f_obj]
    follows.append(username)
    posts= db.session.query(post).filter(post.author.in_(follows))
    return list(posts)

def get_Comments(postid):
    comms= comment.query.filter_by(post=postid).all()
    return comms

def add_Comment(username, postid, caption):
    c = comment(author=username, post=postid, caption=caption, datetime=str(datetime.datetime.now())[:-10])
    db.session.add(c)
    db.session.commit()
    comm = comment.query.order_by(comment.id.desc()).first()
    return comm.id

def delete_Comment(id):
    c = comment.query.filter_by(id=id).first()
    db.session.delete(c)
    db.session.commit()

def search_dao(name):
    users = user.query.filter(user.username.startswith(name)).all()
    return users

@cache.memoize(10)
def get_followers(name):
    followers= follower.query.filter_by(following=name).all()
    followers= [obj.person for obj in followers]
    return followers

@cache.memoize(10)
def get_followings(name):
    followings = follower.query.filter_by(person=name).all()
    followings= [obj.following for obj in followings]
    return followings

def get_posts(name):
    posts= post.query.filter_by(author=name).all()
    return posts

def follow_dao(person, other):
    f_obj= follower(person=person, following=other, datetime=str(datetime.datetime.now())[:-10])
    db.session.add(f_obj)
    db.session.commit()

def unfollow_dao(person, other):
    f_obj = follower.query.filter_by(person=person,following=other).first()
    db.session.delete(f_obj)
    db.session.commit()

def upload_post(username,filename,content,title):
    from models import post
    post = post(author=username, image=filename, caption=content, datetime=str(datetime.datetime.now())[:-10], title=title)
    db.session.add(post)
    db.session.commit()

def edit_post(postid,title,caption):
    post_obj = post.query.filter_by(id=postid).first()
    post_obj.title=title
    post_obj.caption=caption
    post_obj.datetime=str(datetime.datetime.now())[:-10]
    db.session.commit()

def delete_post(postid, username):
    post_obj = post.query.filter_by(id=postid).first()
    if post_obj and (post_obj.author == username):
        comment.query.filter_by(post=postid).delete()
        post.query.filter_by(id=postid).delete()
        db.session.delete(post_obj)
        db.session.commit()
        return True
    else:
        return False

@cache.memoize(10)
def get_post(postid):
    post_obj = post.query.filter_by(id=postid).first()
    if post_obj is None: 
        return None
    return post_obj.author , post_obj.title , post_obj.caption

def change_data(username, newname): 
    posts = post.query.filter_by(author=username).all()
    for p in posts:
        p.author= newname
    comments = comment.query.filter_by(author=username).all()
    for c in comments:
        c.author= newname
    followings = follower.query.filter_by(person=username).all()
    for f in followings:
        f.person= newname
    followers = follower.query.filter_by(following=username).all()
    for f in followers:
        f.following= newname
    db.session.commit()

def delete_data(username):
    post.query.filter_by(author=username).delete() 
    comment.query.filter_by(author=username).delete()
    follower.query.filter_by(person=username).delete()
    follower.query.filter_by(following=username).delete()
    db.session.commit()
