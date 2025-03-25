from core import db, cache
import datetime
from core.models.comment import Comment
from core.models.follower import Follower
from core.models.like import Like


class Blog(db.Model):
    __tablename__= "Blog"
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    author= db.Column(db.Integer,db.ForeignKey('User.id'),nullable=False)
    title= db.Column(db.String,nullable=False)
    caption= db.Column(db.String)
    datetime= db.Column(db.String,nullable=False)
    image = db.Column(db.String)

    # @cache.memoize(10)
    def get(postid): # get_post
        post_obj = Blog.query.filter_by(id=postid).first()
        if post_obj is None: 
            return None
        return post_obj.author , post_obj.title , post_obj.caption

    def upload(userid, filename, content, title): # upload_post
        
        p = Blog(author=userid, image=filename, caption=content, datetime=str(datetime.datetime.now())[:-10], title=title)
        db.session.add(p)
        db.session.commit()

    def edit(postid, title, caption): # edit_post
        post_obj = Blog.query.filter_by(id=postid).first()
        post_obj.title=title
        post_obj.caption=caption
        post_obj.datetime=str(datetime.datetime.now())[:-10]
        db.session.commit()
    
    def delete(postid, userid): # delete_post
        post_obj = Blog.query.filter_by(id=postid).first()
        if post_obj and (post_obj.author == userid):
            Comment.query.filter_by(postid =postid).delete()
            Like.query.filter_by(postid =postid).delete()
            Blog.query.filter_by(id=postid).delete()
            db.session.delete(post_obj)
            db.session.commit()
            return True
        return False

    def get_posts(userid):
        return Blog.query.filter_by(author=userid).all()

    @cache.memoize(10)
    def get_home_posts(userid): # home
        f_obj= Follower.query.filter_by(person=userid).all()
        follows = [f.following for f in f_obj]
        follows.append(userid)
        posts= db.session.query(Blog).filter(Blog.author.in_(follows))
        return list(posts)
