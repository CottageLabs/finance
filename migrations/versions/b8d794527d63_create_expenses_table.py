"""create expenses table

Revision ID: b8d794527d63
Revises: 6a2cab1c24ad
Create Date: 2016-01-03 17:12:28.142425

"""

# revision identifiers, used by Alembic.
revision = 'b8d794527d63'
down_revision = '6a2cab1c24ad'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('expenses',
    sa.Column('url', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('category', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('currency', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('dated_on', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('gross_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('manual_sales_tax_amount', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('native_gross_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('native_sales_tax_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('project', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('receipt_reference', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('sales_tax_rate', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('sales_tax_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('user', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('rebill_factor', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('url', name=u'pk_expenses')
    )

def downgrade():
    op.drop_table('expenses')

