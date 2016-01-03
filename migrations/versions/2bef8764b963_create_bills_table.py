"""create bills table

Revision ID: 2bef8764b963
Revises: 22632b38537f
Create Date: 2016-01-03 16:27:51.736140

"""

# revision identifiers, used by Alembic.
revision = '2bef8764b963'
down_revision = '22632b38537f'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('bills',
    sa.Column('url', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('category', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('project', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('comments', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('contact', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('dated_on', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('due_on', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('due_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('paid_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('reference', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('sales_tax_rate', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('sales_tax_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('status', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('total_value', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('url', name=u'pk_bills')
    )

def downgrade():
    op.drop_table('bills')

