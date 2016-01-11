"""create bank_transaction_explanations table

Revision ID: 22632b38537f
Revises: 0c93ca4f89e3
Create Date: 2016-01-03 16:01:25.903685

"""

# revision identifiers, used by Alembic.
revision = '22632b38537f'
down_revision = '0c93ca4f89e3'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('bank_transaction_explanations',
    sa.Column('url', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('bank_transaction', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('bank_account', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('category', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('dated_on', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('gross_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('paid_bill', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('paid_invoice', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('paid_user', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('receipt_reference', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('sales_tax_rate', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('url', name=u'pk_bank_transaction_explanations')
    )


def downgrade():
    op.drop_table('bank_transaction_explanations')
