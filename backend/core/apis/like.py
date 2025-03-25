from flask_restful import  Resource
from core.decorator import token_required
from core.models.like import Like

class LikeResource(Resource):

    @token_required
    def put(token, self, postid):
        print(type(token['id']))
        Like.add(token['id'], postid)
        return {}
        
    @token_required
    def delete(token, self, postid):
        print(type(token['id']))

        Like.delete(token['id'], postid)
        return {}

