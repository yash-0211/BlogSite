from core import db
from core.models import *
from core.models.user import User
from core.models.comment import Comment
from core.models.blog import Blog
from core.models.follower import Follower
from core.models.like import Like

db.create_all()
