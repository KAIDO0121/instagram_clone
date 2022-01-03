from flask_restful import Resource
from flask import request, jsonify, make_response
from model.model import Photo, UserPhoto
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token
from werkzeug.utils import secure_filename
from upload_manager import UploadManager

# upload photo

ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'svg', 'jpg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadPhoto(Resource):

    @classmethod
    @jwt_required()
    def post(cls):
        upload = UploadManager()
        user_id = get_jwt_identity()
        photo = Photo().save()

        m = photo.to_mongo().to_dict()

        user_photo = UserPhoto.objects(
            user_id=user_id
        ).update_one(
            push__photo_ids=str(m.get('_id')),
            upsert=True
        )

        # No file selected
        if 'file' not in request.files:
            return make_response({"msg": f' *** No files Selected'}, 401)

        file_to_upload = request.files['file']
        content_type = request.mimetype

        # if empty files
        if file_to_upload.filename == '':
            return make_response({"msg": f' *** File name must not be empty'}, 401)

        # file uploaded and check
        if file_to_upload and allowed_file(file_to_upload.filename):

            file_name = secure_filename(file_to_upload.filename)

            print(f" *** The file name to upload is {file_name}")
            print(f" *** The file full path  is {file_to_upload}")

            bucket_name = "instagram-clone-photos"

            upload.s3_upload_small_files(
                file_to_upload, bucket_name, file_name, content_type)
            return make_response({"msg": f'Success - {file_to_upload} Is uploaded to {bucket_name}', "user_photo": user_photo}, 200)

        else:
            return make_response({"msg": f'Allowed file type are - jpeg - jpg - png - svg .Please upload proper formats...'}, 200)


# get photo by user id

# get photo by title
