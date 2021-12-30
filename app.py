from flask import Flask
from flask_mongoengine import MongoEngine
from flask_restful import Api
from api.user import User

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/db"
api = Api(app)
db = MongoEngine(app)
api.add_resource(User, '/products')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)