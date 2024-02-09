from flask import current_app, Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog2.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='secret'

app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/1"
app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/2"

app.config["CACHE_TYPE"] = "RedisCache"
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config["CACHE_REDIS_URL"] = "redis://localhost:6379/0"
app.config['CACHE_DEFAULT_TIMEOUT'] = 500

app.app_context().push()

db=SQLAlchemy()
db.init_app(app)

class user(db.Model, UserMixin):
    __tablename__= "user"
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String,nullable=False,unique=True)
    email= db.Column(db.String,nullable=True)
    password=db.Column(db.String,nullable=False)

class post(db.Model):
    __tablename__= "post"
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    author= db.Column(db.String,db.ForeignKey('user.username'),nullable=False)
    title= db.Column(db.String,nullable=False)
    caption= db.Column(db.String)
    datetime= db.Column(db.String,nullable=False)
    image = db.Column(db.String)

class follower(db.Model):
    # The "person" follows "following". Means person is follower of "following"
    __tablename__= "follower"
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    person= db.Column(db.String,db.ForeignKey("user.username"), nullable=False)
    following= db.Column(db.String, db.ForeignKey("user.username"), nullable=False)
    datetime= db.Column(db.String,nullable=False)

class comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String,db.ForeignKey("user.username"), nullable=False)
    post = db.Column(db.Integer,db.ForeignKey("post.id"), nullable=False)
    caption = db.Column(db.String, nullable=False)
    datetime= db.Column(db.String,nullable=False)

class like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String,db.ForeignKey("user.username"), nullable=False)
    post = db.Column(db.Integer,db.ForeignKey("post.id"), nullable=False)

print("models.py executed")