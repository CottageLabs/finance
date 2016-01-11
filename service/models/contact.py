from service.db import db
from datetime import datetime


class Contact(db.Model):
    __tablename__ = 'contacts'
    url = db.Column(db.String(), nullable=False, primary_key=True)
    account_balance = db.Column(db.Numeric(precision=10, scale=2))
    address1 = db.Column(db.String())
    address2 = db.Column(db.String())
    address3 = db.Column(db.String())
    billing_email = db.Column(db.String())
    charge_sales_tax = db.Column(db.String())
    contact_name_on_invoices = db.Column(db.Boolean())
    country = db.Column(db.String())
    email = db.Column(db.String())
    first_name = db.Column(db.String())
    is_deletable = db.Column(db.Boolean())
    last_name = db.Column(db.String())
    locale = db.Column(db.String())
    mobile = db.Column(db.String())
    phone_number = db.Column(db.String())
    organisation_name = db.Column(db.String())
    postcode = db.Column(db.String())
    region = db.Column(db.String())
    status = db.Column(db.String())
    sales_tax_registration_number = db.Column(db.String())
    town = db.Column(db.String())
    uses_contact_invoice_sequence = db.Column(db.Boolean())
    active_projects_count = db.Column(db.Integer())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, created_at=datetime.now(), updated_at=datetime.now(), **kwargs):
        """Mostly rely on default declarative SQLAlchemy constructor. Additionally set the timestamps on object creation."""
        super(User, self).__init__(**kwargs)  # use the default declarative constructor
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<url {}>'.format(self.url)
