from service.db import db
from datetime import datetime


class BankTransaction(db.Model):
    __tablename__ = 'bank_transactions'
    url = db.Column(db.String(), nullable=False, primary_key=True)
    bank_account = db.Column(db.String())
    amount = db.Column(db.Numeric(precision=10, scale=2))
    dated_on = db.Column(db.Date())
    description = db.Column(db.String())
    full_description = db.Column(db.String())
    is_manual = db.Column(db.Boolean())
    unexplained_amount = db.Column(db.Numeric(precision=10, scale=2))
    uploaded_at = db.Column(db.Date())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, created_at=datetime.now(), updated_at=datetime.now(), **kwargs):
        """Mostly rely on default declarative SQLAlchemy constructor. Additionally set the timestamps on object creation."""
        super(User, self).__init__(**kwargs)  # use the default declarative constructor
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<url {}>'.format(self.url)