from service.database import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = 'categories'

    url = db.Column(db.String(255), nullable=False, primary_key=True)
    allowable_for_tax = db.Column(db.Boolean())
    auto_sales_tax_rate = db.Column(db.String(255))
    description = db.Column(db.String(255))
    group_description = db.Column(db.String(255))
    nominal_code = db.Column(db.String(255))
    tax_reporting_name = db.Column(db.String(255))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, created_at=datetime.now(), updated_at=datetime.now(), **kwargs):
        """Mostly rely on default declarative SQLAlchemy constructor. Additionally set the timestamps on object creation."""
        super(Category, self).__init__(**kwargs)  # use the default declarative constructor
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<url {}>'.format(self.url)
