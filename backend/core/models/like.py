from core import db

class Like(db.Model):
    __tablename__ = 'Like'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.Integer,db.ForeignKey("User.id"), nullable=False)
    postid = db.Column(db.Integer,db.ForeignKey("Blog.id"), nullable=False)


    def add(userid, postid):
        islike = Like.query.filter_by(postid =postid, author=userid).first()
        if islike:
            return
        l = Like(author=userid, postid =postid)
        db.session.add(l)
        db.session.commit()


    def delete(userid, postid):
        l = Like.query.filter_by(postid =postid, author=userid).first()
        if l:
            db.session.delete(l)
            db.session.commit()


    def get_likes(postid):
        likes = Like.query.filter_by(postid=postid).all()
        likes = [l.author for l in likes]
        return likes
