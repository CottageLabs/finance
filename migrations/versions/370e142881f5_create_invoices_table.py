"""create invoices table

Revision ID: 370e142881f5
Revises: b8d794527d63
Create Date: 2016-01-03 17:25:40.702078

"""

# revision identifiers, used by Alembic.
revision = '370e142881f5'
down_revision = 'b8d794527d63'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('invoices',
    sa.Column('url', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('always_show_bic_and_iban', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('comments', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('contact', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('currency', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('dated_on', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('discount_percent', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('due_on', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('due_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('exchange_rate', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('involves_sales_tax', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('is_interim_uk_vat', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('net_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('omit_header', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('paid_on', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('paid_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('payment_terms_in_days', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('po_reference', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('project', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('reference', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('sales_tax_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('show_project_name', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('total_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('written_off_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('send_reminder_emails', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('send_thank_you_emails', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('send_new_invoice_emails', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('include_timeslips', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('recurring_invoice', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('billed_grouped_by_single_timeslip', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('bank_account', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('client_contact_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('url', name=u'pk_invoices')
    )


def downgrade():
    op.drop_table('invoices')
