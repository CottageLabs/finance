from service.db import db
from datetime import datetime


class Invoice(db.Model):
    __tablename__ = 'invoices'
    url = db.Column(db.String(), nullable=False, primary_key=True)
    always_show_bic_and_iban = db.Column(db.Boolean())
    comments = db.Column(db.String())
    contact = db.Column(db.String())
    currency = db.Column(db.String())
    dated_on = db.Column(db.Date())
    discount_percent = db.Column(db.Numeric(precision=10, scale=2))
    due_on = db.Column(db.Date())
    due_value = db.Column(db.Numeric(precision=10, scale=2))
    exchange_rate = db.Column(db.Numeric(precision=10, scale=2))
    involves_sales_tax = db.Column(db.Boolean())
    is_interim_uk_vat = db.Column(db.Boolean())
    net_value = db.Column(db.Numeric(precision=10, scale=2))
    omit_header = db.Column(db.Boolean())
    paid_on = db.Column(db.Date())
    paid_value = db.Column(db.Numeric(precision=10, scale=2))
    payment_terms_in_days = db.Column(db.Integer())
    po_reference = db.Column(db.String())
    project = db.Column(db.String())
    reference = db.Column(db.String())
    sales_tax_value = db.Column(db.Numeric(precision=10, scale=2))
    show_project_name = db.Column(db.Boolean())
    status = db.Column(db.String())
    total_value = db.Column(db.Numeric(precision=10, scale=2))
    written_off_date = db.Column(db.Date())
    send_reminder_emails = db.Column(db.Boolean())
    send_thank_you_emails = db.Column(db.Boolean())
    send_new_invoice_emails = db.Column(db.Boolean())
    include_timeslips = db.Column(db.String())
    recurring_invoice = db.Column(db.String())
    billed_grouped_by_single_timeslip = db.Column(db.Boolean())
    bank_account = db.Column(db.String())
    client_contact_name = db.Column(db.String())
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())

    def __init__(self, created_at=datetime.now(), updated_at=datetime.now(), **kwargs):
        """Mostly rely on default declarative SQLAlchemy constructor. Additionally set the timestamps on object creation."""
        super(User, self).__init__(**kwargs)  # use the default declarative constructor
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return '<url {}>'.format(self.url)
