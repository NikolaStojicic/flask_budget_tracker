from flask_restplus import Resource, Api
from werkzeug.datastructures import FileStorage
import os
from werkzeug.utils import secure_filename
from flask import send_file

api = Api()
upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


def file_save(file):
    new_filename = secure_filename(file.filename)
    file_path = os.path.join(os.curdir + '\\files\\', new_filename)
    file.save(file_path)
    return file_path


@api.expect(upload_parser)
class FileUpload(Resource):
    def post(self):
        uploaded_file = upload_parser.parse_args()['file']
        file_save(uploaded_file)
        return {'msg': 'File uploaded!'}, 200


class FileGet(Resource):
    def get(self, imgname):
        path = os.path.abspath('files')
        try:
            return send_file(
                f'{path}\\{imgname}')
        except FileNotFoundError:
            return {'msg': 'File not found!'}, 404
