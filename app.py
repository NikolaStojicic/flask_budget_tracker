from flask import Flask
from flask_restplus import Resource, Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister, Users, UserLogin, TokenRefresh
from resources.ticket import TicketResource
from flask_cors import CORS
from resources.file import FileUpload, FileGet

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'rofl_security_please'
api = Api(app)

jwt = JWTManager(app)
jwt._set_error_handler_callbacks(api)


@app.before_first_request
def create_tables():
    db.create_all()


class Ping(Resource):
    def get(self):
        return {'msg': 'Server is online!'}, 200


api.add_resource(Ping, '/ping')
api.add_resource(UserRegister, '/register')
api.add_resource(Users, '/users')
api.add_resource(TicketResource, '/ticket/<int:_id>', '/ticket')
api.add_resource(UserLogin, '/login')
api.add_resource(FileUpload, '/file')
api.add_resource(FileGet, '/file/<string:imgname>')
api.add_resource(TokenRefresh, '/refreshjwt')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', debug=True)
