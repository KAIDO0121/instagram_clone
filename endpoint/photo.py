from flask_restful import Resource
from flask import request, jsonify
from model.model import Photo, UserPhoto
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
from app import storage_client

# upload photo

ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'gif', 'jpg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadPhoto(Resource):

    @classmethod
    @jwt_required()
    def post(cls):
        user_id = get_jwt_identity()

        photo_to_upload = request.files['file']

        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        if photo_to_upload.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp

        if photo_to_upload and allowed_file(photo_to_upload.filename):
            photo = Photo(photo_name=photo_to_upload.filename).save()
            m = photo.to_mongo().to_dict()
            user_photo = UserPhoto.objects(
                user_id=user_id
            ).update_one(
                push__photo_ids=str(m.get('_id')),
                push__photo_names=photo_to_upload.filename,
                upsert=True
            )
            filename = secure_filename(photo_to_upload.filename)
            bucket = storage_client.bucket('instagram-clone-photos')
            blob = bucket.blob(filename)
            blob.chunk_size = 1024 * 1024
            blob.upload_from_file(photo_to_upload)

            resp = jsonify({'message': f'{ filename } successfully uploaded'})
            resp.status_code = 201

        else:
            resp = jsonify(
                {'message': 'Allowed file types are png, jpg, jpeg, gif'})
            resp.status_code = 400

        return resp

# get photo by user id

# get photo by title
