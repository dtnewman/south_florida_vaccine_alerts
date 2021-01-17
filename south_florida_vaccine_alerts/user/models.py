import bcrypt
import datetime
import flask
from flask_login import UserMixin
import sqlalchemy

from south_florida_vaccine_alerts.extensions import db


class User(db.Model, UserMixin):

    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(200), unique=False, nullable=False)
    phone = sqlalchemy.Column(sqlalchemy.String(20), unique=False, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(80), unique=True, nullable=False)
    sms_consent = sqlalchemy.Column(sqlalchemy.Boolean, unique=True, nullable=False)

    created_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, name, phone, email, sms_consent):
        self.name = name
        self.phone = phone
        self.email = email
        self.sms_consent = sms_consent

    @staticmethod
    def create(session, name, phone, email, sms_consent):
        user = User(name, phone, email, sms_consent)
        session.add(user)
        session.flush()
        return user

    @classmethod
    def get_by_id(cls, session, user_id):
        if any(
            (isinstance(user_id, str) and user_id.isdigit(),
             isinstance(user_id, (int, float))),
        ):
            return session.query(cls).filter(cls.id == user_id).first()
        return None

    def __repr__(self):
        return '<User({id!r})>'.format(id=self.username)
