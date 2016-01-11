from service.db import db
from datetime import datetime


class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'

    url = db.Column(db.String(), nullable=False, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    role = db.Column(db.String())
    permission_level = db.Column(db.Integer())
    opening_mileage = db.Column(db.Numeric(precision=10, scale=2))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, created_at=datetime.now(), updated_at=datetime.now(), **kwargs):
        """Mostly rely on default declarative SQLAlchemy constructor. Additionally set the timestamps on object creation."""
        super(User, self).__init__(**kwargs)  # use the default declarative constructor
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<url {}>'.format(self.url)