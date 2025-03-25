from flask_restful import  Resource 
from core.decorator import token_required
from core.models.follower import Follower
from core.models.user import User


class FollowResource(Resource):

    @token_required
    def post(token, self, other_user): # follow
        person = token['id']
        other_user = User.get_by_username(other_user).get_id()
        if person == other_user:
            return {"message":"You cannot follow yourself"},
        Follower.follow(person, other_user)
        return {}
    
    @token_required
    def delete(token, self, other_user): # unfollow
        person = token['id']
        other_user = User.get_by_username(other_user).get_id()
        if person == other_user:
            return {"message":"You cannot follow yourself"},
        Follower.unfollow(person, other_user)
        return {}
