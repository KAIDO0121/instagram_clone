from app import db
from datetime import datetime

# Important: In MongoDB, a collection is not created until it gets content!

class User(db.Document):
    name = db.StringField()
    creation_date = db.DateTimeField(default=datetime.utcnow)
    last_login = db.DateTimeField()

class Photo(db.Document):
    creation_date = db.DateTimeField(default=datetime.utcnow)
    photo_path = db.StringField()

    # because upload photo would be slow, so we are separating it from downloading and searching photos 
    # for upload:
    #   user writing photo path to db A
    #   user upload photo to file storage B 

    # for download( view ):
    #   user query photo path from db A
    #   user use the path to download photo from file storage B

class UserPhoto(db.Document):
    user_id = db.ObjectIdField(primary_key= True)
    photo_ids = db.ListField()

class Follow(db.Document):
    is_following = db.ObjectIdField()
    user_id = db.ObjectIdField()

class UserFollow(db.Document):
    user_id = db.ObjectIdField(primary_key= True)
    is_followed_by_ids = db.ListField()
    following_ids = db.ListField()