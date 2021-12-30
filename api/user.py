from flask_restful import Resource
from flask import request

# follow other user
# 
# get all followees by user id
# 
# register
#
# login

class FollowUser(Resource):
    @classmethod
    def post(self):
        return 

class GetAllFollowees(Resource):
    @classmethod
    def get(self):
        return 

class Register(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = User(**body).save()
        return 

class Login(Resource):
    @classmethod
    def post(cls):
        return 