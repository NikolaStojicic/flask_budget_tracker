from db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))

    def json(self):
        return {'name': self.name, 'pw': self.password}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(name=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
