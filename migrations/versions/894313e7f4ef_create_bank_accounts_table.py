"""create bank_accounts table

Revision ID: 894313e7f4ef
Revises: 20c57cc7e57b
Create Date: 2015-12-31 11:13:13.855067

"""

# revision identifiers, used by Alembic.
revision = '894313e7f4ef'
down_revision = '20c57cc7e57b'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank_accounts',
    sa.Column('url', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('account_number', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('bank_code', sa.VARCHAR(length=25), autoincrement=False, nullable=True),
    sa.Column('bank_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('bic', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('latest_activity_date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('currency', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('current_balance', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('iban', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('is_personal', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('is_primary', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('opening_balance', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('sort_code', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('type', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('url', name=u'pk_bank_accounts')
    )

def downgrade():
    op.drop_table('bank_accounts')
