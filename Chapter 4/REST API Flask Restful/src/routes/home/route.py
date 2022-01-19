from flask_restful import Resource
from flask import request
from utils.models.user import User
from utils.db import db

class HomeRoute(Resource):
    def get(self):
        users = db.session.query(User).all()
        users = [user.to_json() for user in users]
        return {'data': users}

    def post(self):
        name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        user = User(first_name=name, last_name=last_name, email=email)
        db.session.add(user) # add user to database
        db.session.commit() # commit the changes to the database"""
        return {'data': user.to_json()}



class HomeRouteWithId(Resource):
    def get(self, id):
        data_object = db.session.query(User).filter(User.user_id == id).first()
        if data_object:
            return {"data": data_object.to_json()}
        else:
            return {"data": "Not Found"}, 404

    def put(self, id):
        data_object = db.session.query(User).filter(User.user_id == id).first()
        if data_object:
            for key in request.form.keys():
                setattr(data_object, key, request.form[key])
            db.session.commit()
            return {"data": data_object.to_json()}
        else:
            return {"data": "Not Found"}, 404

    def delete(self, id):
        data_object = db.session.query(User).filter(User.user_id == id).first()
        if data_object:
            db.session.delete(data_object)
            db.session.commit()
            return {"data": "DELETED"}
        else:
            return {"data": "Not Found"}, 404
