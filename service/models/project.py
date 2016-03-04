from service.db import db
from datetime import datetime


class Project(db.Model):
    __tablename__ = 'projects'

    url = db.Column(db.String(), nullable=False, primary_key=True)
    name = db.Column(db.String())
    contact = db.Column(db.String())
    budget = db.Column(db.Integer())
    is_ir35 = db.Column(db.Boolean())
    status = db.Column(db.String())
    budget_units = db.Column(db.String())
    normal_billing_rate = db.Column(db.Column(db.Numeric(precision=10, scale=2)))
    hours_per_day = db.Column(db.Column(db.Numeric(precision=10, scale=2)))
    uses_project_invoice_sequence = db.Column(db.Boolean())
    currency = db.Column(db.String())
    billing_period = db.Column(db.String())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, created_at=datetime.now(), updated_at=datetime.now(), **kwargs):
        """Mostly rely on default declarative SQLAlchemy constructor. Additionally set the timestamps on object creation."""
        super(Project, self).__init__(**kwargs)  # use the default declarative constructor
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<url {}>'.format(self.url)