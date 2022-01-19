from flask import Flask
from flask_restful import Api
from routes.home.route import HomeRoute, HomeRouteWithId
from utils.db import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    api = Api(app)
    db.init_app(app) # initialize the database
    db.create_all(app=app) # create tables
    api.add_resource(HomeRoute, '/')
    api.add_resource(HomeRouteWithId, '/<string:id>')
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
