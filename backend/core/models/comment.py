from core import db

import datetime


class Comment(db.Model):
    __tablename__ = 'Comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.Integer,db.ForeignKey("User.id"), nullable=False)
    postid = db.Column(db.Integer,db.ForeignKey("Blog.id"), nullable=False)
    caption = db.Column(db.String, nullable=False)
    datetime= db.Column(db.String,nullable=False)

    def add(userid, postid, caption): # add_Comment
        c = Comment(author=userid, postid=postid, caption=caption, datetime=str(datetime.datetime.now())[:-10])
        db.session.add(c)
        db.session.commit()
        comm = Comment.query.order_by(Comment.id.desc()).first()
        return comm.id
    
    def delete(id): # delete_Comment
        c = Comment.query.filter_by(id=id).first()
        db.session.delete(c)
        db.session.commit()
    
    def get_list(postid): # get_Comments
        return Comment.query.filter_by(postid=postid).all()
