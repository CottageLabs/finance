from service.db import db
from datetime import datetime


class Expense(db.Model):
    __tablename__ = 'expenses'
    url = db.Column(db.String(), nullable=False, primary_key=True)
    category = db.Column(db.String())
    currency = db.Column(db.String())
    dated_on = db.Column(db.Date())
    description = db.Column(db.String())
    gross_value = db.Column(db.Numeric(precision=10, scale=2))
    manual_sales_tax_amount = db.Column(db.Numeric(precision=10, scale=2))
    native_gross_value = db.Column(db.Numeric(precision=10, scale=2))
    native_sales_tax_value = db.Column(db.Numeric(precision=10, scale=2))
    project = db.Column(db.String())
    receipt_reference = db.Column(db.String())
    sales_tax_rate = db.Column(db.Numeric(precision=10, scale=2))
    sales_tax_value = db.Column(db.Numeric(precision=10, scale=2))
    user = db.Column(db.String())
    rebill_factor = db.Column(db.Numeric(precision=10, scale=2))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, created_at=datetime.now(), updated_at=datetime.now(), **kwargs):
        """Mostly rely on default declarative SQLAlchemy constructor. Additionally set the timestamps on object creation."""
        super(Expense, self).__init__(**kwargs)  # use the default declarative constructor
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<url {}>'.format(self.url)
