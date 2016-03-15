from service.db import db
from datetime import datetime


class Bill(db.Model):
    __tablename__ = 'bills'
    url = db.Column(db.String(), nullable=False, primary_key=True)
    category = db.Column(db.String())
    project = db.Column(db.String())
    comments = db.Column(db.String())
    contact = db.Column(db.String())
    dated_on = db.Column(db.Date())
    due_on = db.Column(db.Date())
    due_value = db.Column(db.Numeric(precision=10, scale=2))
    paid_value = db.Column(db.Numeric(precision=10, scale=2))
    reference = db.Column(db.String())
    sales_tax_rate = db.Column(db.Numeric(precision=10, scale=2))
    sales_tax_value = db.Column(db.Numeric(precision=10, scale=2))
    status = db.Column(db.String())
    total_value = db.Column(db.Numeric(precision=10, scale=2))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, created_at=datetime.now(), updated_at=datetime.now(), **kwargs):
        """Mostly rely on default declarative SQLAlchemy constructor. Additionally set the timestamps on object creation."""
        super(Bill, self).__init__(**kwargs)  # use the default declarative constructor
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<url {}>'.format(self.url)
