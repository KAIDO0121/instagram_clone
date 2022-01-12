from caches.recent_visit_users import RECENT_VISITED_USERS
from model.model import UserFollow, UserPhoto
from app import storage_client
import threading


class NewsFeed:

    def __init__(self) -> None:
        self.recent_visited_users = RECENT_VISITED_USERS
        self.active_user_followings = []
        self.most_recent_photos = []

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
        # {}
        all_follows = []
        for _, active_id in RECENT_VISITED_USERS.get_dict():
            print(type(UserFollow.objects(user_id=active_id).first().following_ids))
            all_follows.append(
                {active_id: UserFollow.objects(user_id=active_id).first().following_ids})
        self.active_user_followings = all_follows

    def get_following_photos(self):
        following_photos = []
        # generate photo of followings per active user

        for following_relationship in self.active_user_followings:

            user_photo_names = []

            # for k, v in following_relationship.items():
            # a = UserPhoto.objects(user_id=v)
            # print(v)
            # user_photo_names.append(*a)

            for user_photo_name in user_photo_names:
                bucket = storage_client.bucket('instagram-clone-photos')
                blob = bucket.blob(user_photo_name)
                contents = blob.download_as_string()
                following_photos.append(contents)

        print(following_photos)


# given a time interval
#   get recent active users
#   get all user following
#   get popular photos from user followings
#       rank by photo meta datas ( from meta DB )
#   store in cache
