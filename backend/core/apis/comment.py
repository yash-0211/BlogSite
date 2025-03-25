from flask_restful import  Resource 
from core.decorator import token_required
import json 
import os 
from flask import request
from core.models.user import User
from core.models.comment import Comment


class CommentResource(Resource):

    @token_required
    def put(token, self, id):
        data = json.loads(request.data)
        postid = data.get("postid", None)
        userid = token['id']
        username= token['username']
        newComment= data.get("newComment", None)
        print(newComment)
        comm_id= Comment.add(userid, postid, newComment)
        ispic= os.path.exists(f"static/img/propics/{userid}.jpg")
        dict={"comment":{ "id":comm_id, "author":username, "caption": newComment, "userid":"", "ispic": ispic,
                        "userid": userid, "ispic": ispic}}
        return dict
    
    @token_required
    def delete(token, self, id):
        Comment.delete(id)
        return {}


class CommentListResource(Resource):

    def get(self, postid):
        comms= Comment.get_list(postid)
        dict={"comments":[]}
        for comm in comms:
            id = comm.author
            author = User.query.filter_by(id=id).first().username
            obj= {"id":comm.id, "author":author, "caption":comm.caption, "userid":id,
                "ispic":os.path.exists(f"static/img/propics/{id}.jpg"),
                }
            dict["comments"].append(obj)
        return dict
