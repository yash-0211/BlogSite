from core import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from core.models.comment import Comment
from core.models.blog import Blog
from core.models.follower import Follower
from core.models.like import Like


class User(db.Model, UserMixin):
    __tablename__= "User"
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String,nullable=False,unique=True)
    email= db.Column(db.String,nullable=True)
    password=db.Column(db.String,nullable=False)

    def create(name, email, password): # create_user_dao
        u_obj = User(username=name, password=generate_password_hash(password), email=email)
        db.session.add(u_obj)
        db.session.commit()
        return u_obj

    def get_id(self):
        return self.id
    
    def get_by_id(id): # get_user
        return User.query.filter_by(id=id).first()
    
    def get(name): # get_user
        return User.query.filter_by(username=name).first()
    
    def get_by_email(email): # get_user_by_email
        return User.query.filter_by(email=email).first()
    
    def get_by_username(username): # get_user_by_username
        return User.query.filter_by(username=username).first()
    
    def alreadyExist(name,email):
        e = User.query.filter_by(email=email).first()
        u = User.query.filter_by(username=name).first()
        if u: return "username"
        if e: return "email"
        return None
    
    def update_name(username, newname):  # change_data
        blogs = Blog.query.filter_by(author=username).all()
        for p in blogs:
            p.author= newname
        comments = Comment.query.filter_by(author=username).all()
        for c in comments:
            c.author= newname
        likes = Like.query.filter_by(author=username).all()
        for l in likes:
            l.author= newname
        followings = Follower.query.filter_by(person=username).all()
        for f in followings:
            f.person= newname
        followers = Follower.query.filter_by(following=username).all()
        for f in followers:
            f.following= newname
        db.session.commit()
    
    def delete(username):
        Blog.query.filter_by(author=username).delete() 
        Comment.query.filter_by(author=username).delete()
        Like.query.filter_by(author=username).delete()
        Follower.query.filter_by(person=username).delete()
        Follower.query.filter_by(following=username).delete()
        User.query.filter_by(username=username).delete()
        db.session.commit()
    
    def search(name): # search_dao
        return User.query.filter(User.username.startswith(name)).all()
