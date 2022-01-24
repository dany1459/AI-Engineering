from flask import Flask, render_template, request, redirect
from flask_restful import Resource, Api
from routes.home.route import HomeRoute, FilmWithId, FilmCommentWithId
from utils.db import db
import requests
import json

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    api = Api(app)

    db.init_app(app) #initialize the database
    db.create_all(app=app) #create tables

    api.add_resource(HomeRoute, '/data')
    api.add_resource(FilmWithId, '/<string:movie_id>')
    api.add_resource(FilmCommentWithId, '/comment/<string:comment_id>')
    return app



if __name__ == '__main__':
    app = create_app()

    @app.route('/', methods=['GET'])
    def home():
        req = requests.get('http://127.0.0.1:5000/data')
        data = json.loads(req.content)
        return render_template('home.html', data=data)


    @app.route("/movie/<imdbid>", methods=["GET","POST"])
    def film_detail(imdbid):

        URL = f'http://www.omdbapi.com/?i={imdbid}&apikey=fb4d7ea8'
        r = requests.get(URL)
        movie = r.json()

        if request.method == 'POST':
            text = request.form.get('text')
            data = {'text':text}
            requests.post(f'http://127.0.0.1:5000/{imdbid}',data=data)
            return redirect(f'http://127.0.0.1:5000/movie/{imdbid}')

        req = requests.get(f'http://127.0.0.1:5000/{imdbid}')
        if req.status_code == 404:
            all_comments = {'data': []}
        else:
            all_comments = json.loads(req.content)


        return render_template("film_detail.html", all_comments=all_comments, movie=movie)


    app.run(debug=True)