from db import db


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    description = db.Column(db.String(500))
    image = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User')

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'image': self.image
        }

    @classmethod
    def find_by_id(cls, _id, user_id):
        return cls.query.filter_by(id=_id).filter_by(user_id=user_id).first()
