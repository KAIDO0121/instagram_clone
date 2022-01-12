from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_jwt_extended import JWTManager
from google.cloud import storage
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/liaoyushun/Desktop/credentials/instagram-clone-337113-d40a109cb7f5.json"
db = MongoEngine()
storage_client = storage.Client()


def create_app():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'db',
        'host': 'localhost',
        'port': 27017
    }
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
    db.init_app(app)
    api = Api(app)
    app.config["JWT_SECRET_KEY"] = "super-secret"

    jwt = JWTManager(app)
    from endpoint.user import Register, FollowUser, GetUserFollows, Login
    from endpoint.photo import UploadPhoto
    from endpoint.newsfeedservice import NewsFeed

    news_feed = NewsFeed()
    news_feed.generate_feed()
    api.add_resource(Login, '/api/login')
    api.add_resource(Register, '/api/register')
    api.add_resource(FollowUser, '/api/followuser')
    api.add_resource(GetUserFollows, '/api/getuserfollows')
    api.add_resource(UploadPhoto, '/api/upload_photo')

    return app


if __name__ == "__main__":
    create_app().run(debug=True, host="0.0.0.0", port=3000)
