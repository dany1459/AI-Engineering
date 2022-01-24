from flask_restful import Resource
from flask import request
import uuid
from utils.models.comments import Comments
from utils.db import db


class HomeRoute(Resource):

    def get(self):
        comments = db.session.query(Comments).all()
        comments = [comment.to_json() for comment in comments]
        return {'data':comments}


class FilmWithId(Resource):
    def get(self, movie_id):
        data_object = db.session.query(Comments).filter(Comments.movie_id == movie_id).all()
        comments_film = [comment.to_json() for comment in data_object]
        if (data_object):
            return {'data':comments_film}
        else:
            return {'data':'Not Found'},404

    def post(self, movie_id):

        text = request.form['text']
        comment = Comments(movie_id=movie_id, text=text)
        db.session.add(comment)
        db.session.commit()
        return {'data': comment.to_json()}

class FilmCommentWithId(Resource):
    def put(self, comment_id):
        data_object = db.session.query(Comments).filter(Comments.comment_id == comment_id).first()
        if (data_object):
            for key in request.form.keys():
                setattr(data_object, key, request.form[key])
            db.session.commit()
            return {'data': data_object.to_json()}
        else:
            return {'data': 'Not Found'}, 404

    def delete(self, comment_id):
        data_object = db.session.query(Comments).filter(Comments.comment_id == comment_id).first()
        if (data_object):
            db.session.delete(data_object)
            db.session.commit()
            return {'data':'DELETED'}
        else:
            return {'data': 'Not Found'}, 404