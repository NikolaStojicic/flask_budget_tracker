from flask_restplus import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.ticket import Ticket
from models.user import User

api = Api()


def create_new_ticket():
    new_ticket = Ticket(name=api.payload['name'], price=api.payload['price'],
                        description=api.payload['description'], image=api.payload['image'],
                        user_id=get_jwt_identity())
    db.session.add(new_ticket)
    db.session.commit()


class TicketResource(Resource):
    @jwt_required
    def post(self):
        if len(api.payload['name']) == 0:
            return {'msg': "Name is mandatory!"}, 400
        create_new_ticket()
        return {'msg': 'New ticket added'}, 200

    @jwt_required
    def get(self, _id=-1):
        tickets = Ticket.query.filter_by(user_id=get_jwt_identity())
        if _id == -1:
            return {'tickets': [ticket.json() for ticket in tickets]}

        for ticket in tickets:
            if ticket.id == _id:
                return {'ticket': ticket.json()}
        return {'msg': "No ticket with such ID!"}, 404

    @jwt_required
    def put(self, _id=-1):
        if _id == -1:
            return {"msg": "Bad request!"}, 401
        current_user_id = get_jwt_identity()
        ticket = Ticket.find_by_id(_id, current_user_id)
        if not ticket:
            return {'msg': 'No such Ticket.'}, 404
        ticket.name = api.payload['name']
        ticket.price = api.payload['price']
        ticket.description = api.payload['description']
        ticket.image = api.payload['image']
        ticket.user_id = get_jwt_identity()
        db.session.commit()
        return {'msg': ticket.json()}

    @jwt_required
    def delete(self, _id=-1):
        if _id == -1:
            return {"msg": "Bad request!"}, 401
        current_user_id = get_jwt_identity()
        ticket = Ticket.find_by_id(_id, current_user_id)
        if not ticket:
            return {'msg': "Ticket doesn't exist!"}, 404
        db.session.delete(ticket)
        db.session.commit()
        return{'msg': "Ticket successfully deleted!"}, 200
