from flask import Flask
from flask_restful import Api, Resource, reqparse
import db

app1 = Flask(__name__)
api = Api(app1)

class Music(Resource):
    def get(self):
        return db.get_music()


class Genre(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("genre", type=str)
        args = parser.parse_args()
        genre = args['genre']

        return db.get_genre(genre)

api.add_resource(Music, "/music")
api.add_resource(Genre, "/genre")

if __name__ == "__main__":
    app1.run('0.0.0.0')

### for images
# docker build -t api . # to build the docker file
# docker rmi api --force # to delete the file
# docker image ls
# docker run -d -p 5000:5000 api # -d=detach, -p=port


### for containers
# docker container ls # get list of container ids
# docker container stop a46r93c3fja = container id

# docker container ls -a # show inactive containers
# docker container rm a46r93c3fja # remove that container
