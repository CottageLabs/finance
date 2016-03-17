from service.database import db
from datetime import datetime


class BankAccount(db.Model):
    __tablename__ = 'bank_accounts'

    url = db.Column('url', db.String(length=255), autoincrement=False, nullable=False, primary_key=True)
    account_number = db.Column('account_number', db.String(length=255), autoincrement=False, nullable=True)
    bank_code = db.Column('bank_code', db.String(length=25), autoincrement=False, nullable=True)
    bank_name = db.Column('bank_name', db.String(length=255), autoincrement=False, nullable=True)
    bic = db.Column('bic', db.String(length=255), autoincrement=False, nullable=True)
    latest_activity_date = db.Column('latest_activity_date', db.DATE(), autoincrement=False, nullable=True)
    currency = db.Column('currency', db.String(length=255), autoincrement=False, nullable=True)
    current_balance = db.Column('current_balance', db.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True)
    iban = db.Column('iban', db.String(length=255), autoincrement=False, nullable=True)
    is_personal = db.Column('is_personal', db.BOOLEAN(), autoincrement=False, nullable=True)
    is_primary = db.Column('is_primary', db.BOOLEAN(), autoincrement=False, nullable=True)
    name = db.Column('name', db.String(length=255), autoincrement=False, nullable=True)
    opening_balance = db.Column('opening_balance', db.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True)
    sort_code = db.Column('sort_code', db.String(length=255), autoincrement=False, nullable=True)
    type = db.Column('type', db.String(length=255), autoincrement=False, nullable=True)
    created_at = db.Column('created_at', db.DateTime(), nullable=True)
    updated_at = db.Column('updated_at', db.DateTime(), nullable=True)

    def __init__(self, created_at=datetime.now(), updated_at=datetime.now(), **kwargs):
        """Mostly rely on default declarative SQLAlchemy constructor. Additionally set the timestamps on object creation."""
        super(BankAccount, self).__init__(**kwargs)  # use the default declarative constructor
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<url {}>'.format(self.url)