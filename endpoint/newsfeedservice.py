from caches.recent_visit_users import RECENT_VISITED_USERS
from model.model import UserFollow, UserPhoto
from app import storage_client
import base64
import threading
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import make_response, jsonify

NEWS_FEED_CACHE = {}


class NewsFeedGenerator:

    def __init__(self) -> None:
        self.recent_visited_users = RECENT_VISITED_USERS
        self.active_user_followings = {}

    def generate_feed(self):
        def cb():
            self.recent_visited_users = RECENT_VISITED_USERS
            self.get_all_followings()
            self.get_following_photos()
        self.set_interval(cb, 10)

    def set_interval(self, func, sec):
        def func_wrapper():
            self.set_interval(func, sec)
            func()
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t

    def get_all_followings(self) -> list:

        for _, active_id in RECENT_VISITED_USERS.get_dict():
            self.active_user_followings[active_id] = UserFollow.objects(
                user_id=active_id).first().following_ids

    def get_following_photos(self):

        for active_user_id, is_followings in self.active_user_followings.items():

            following_photos = []
            user_photo_names = []

            for is_following in is_followings:
                a = getattr(UserPhoto.objects(
                    user_id=is_following
                ).first(), 'photo_names', None)
                if a:
                    user_photo_names.append(*a)

            for user_photo_name in user_photo_names:
                if user_photo_name:
                    bucket = storage_client.bucket('instagram-clone-photos')
                    blob = bucket.blob(user_photo_name)
                    # sort with blob.updated
                    contents = blob.download_as_bytes()
                    img = "data:image/png;base64, " + \
                        base64.b64encode(contents).decode('ascii')
                    following_photos.append(img)
                else:
                    following_photos.append(None)

            NEWS_FEED_CACHE[active_user_id] = following_photos


class GetNewsFeedByUserId(Resource):

    @classmethod
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        print(RECENT_VISITED_USERS.get_dict())
        return make_response(jsonify(NEWS_FEED_CACHE.get(user_id)), 201)

# given a time interval
#   get recent active users
#   get all user following
#   get popular photos from user followings
#       rank by photo meta datas ( from meta DB )
#   store in cache
