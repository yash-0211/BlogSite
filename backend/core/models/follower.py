from core import db, cache
import datetime


class Follower(db.Model):
    # The "person" follows "following". Means person is follower of "following"
    __tablename__= "Follower"
    id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    person= db.Column(db.Integer,db.ForeignKey("User.id"), nullable=False)
    following= db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    datetime= db.Column(db.String,nullable=False)

    def follow(person, other): # follow_dao
        f_obj= Follower.query.filter_by(person=person,following= other).first()
        if not f_obj:
            f_obj= Follower(person=person, following=other, datetime=str(datetime.datetime.now())[:-10])
            db.session.add(f_obj)
            db.session.commit()

    def unfollow(person, other):
        f_obj = Follower.query.filter_by(person=person,following=other).first()
        db.session.delete(f_obj)
        db.session.commit()
    
    # @cache.memoize(10)
    def get_followers(userid):
        followers= Follower.query.filter_by(following=userid).all()
        followers= [obj.person for obj in followers]
        return followers

    @cache.memoize(10)
    def get_followings(userid):
        followings = Follower.query.filter_by(person=userid).all()
        followings= [obj.following for obj in followings]
        return followings

