"""create contacts table

Revision ID: 6a2cab1c24ad
Revises: 2bef8764b963
Create Date: 2016-01-03 16:42:26.128902

"""

# revision identifiers, used by Alembic.
revision = '6a2cab1c24ad'
down_revision = '2bef8764b963'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('contacts',
    sa.Column('url', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('account_balance', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('address1', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('address2', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('address3', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('billing_email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('charge_sales_tax', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('contact_name_on_invoices', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('country', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('is_deletable', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('locale', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('mobile', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('phone_number', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('organisation_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('postcode', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('region', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('sales_tax_registration_number', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('town', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('uses_contact_invoice_sequence', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('active_projects_count', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('url', name=u'pk_contacts')
    )

def downgrade():
    op.drop_table('contacts')
