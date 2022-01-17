from flask_restful import Resource
from flask import request, jsonify, make_response
from model.model import User, Follow, UserFollow
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token
from caches.recent_visit_users import RECENT_VISITED_USERS

USER_ALREADY_EXISTS = "A user with that username already exists."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."
EMAIL_ALREADY_EXISTS = "Email already exists."


class FollowUser(Resource):

    @classmethod
    @jwt_required()
    def post(cls):
        payload_json = request.get_json()
        user_id = get_jwt_identity()
        follow = Follow(user_id=user_id,
                        is_following=payload_json["is_following"]).save()
        user_follow = UserFollow.objects(
            user_id=user_id
        ).update_one(
            push__following_ids=payload_json["is_following"],
            upsert=True)

        been_followed = UserFollow.objects(
            user_id=payload_json["is_following"]
        ).update_one(
            push__is_followed_by_ids=user_id,
            upsert=True
        )

        return make_response(jsonify(follow, user_follow, been_followed), 201)


class GetUserFollows(Resource):

    @classmethod
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        all_follows = UserFollow.objects(user_id=user_id)
        return make_response(jsonify(all_follows), 201)


class Register(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = User(name=user_json["name"]).save()

        m = user.to_mongo().to_dict()

        access_token = create_access_token(
            identity=str(m.get('_id')), fresh=True)
        refresh_token = create_refresh_token(str(m.get('_id')))

        RECENT_VISITED_USERS.put(user_json['name'], str(m.get('_id')))
        # added this line just for development
        return make_response({"access_token": access_token, "refresh_token": refresh_token, "user": user}, 201)


class Login(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = User.objects.get(name=user_json['name'])
        m = user.to_mongo().to_dict()
        if user:
            access_token = create_access_token(
                identity=str(m.get('_id')), fresh=True)
            refresh_token = create_refresh_token(str(m.get('_id')))
            RECENT_VISITED_USERS.put(user_json['name'], str(m.get('_id')))
            return {"access_token": access_token, "refresh_token": refresh_token, "errorCode": 0}, 200
        if not user:
            return {"message": "User name not found", "errorCode": 2}, 200

        return {"message": INVALID_CREDENTIALS, "errorCode": 1}, 200
