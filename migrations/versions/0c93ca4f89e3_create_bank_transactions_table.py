"""create bank_transactions table

Revision ID: 0c93ca4f89e3
Revises: 894313e7f4ef
Create Date: 2016-01-03 15:30:32.066896

"""

# revision identifiers, used by Alembic.
revision = '0c93ca4f89e3'
down_revision = '894313e7f4ef'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table('bank_transactions',
    sa.Column('url', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('bank_account', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('amount', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('dated_on', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('full_description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('is_manual', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('unexplained_amount', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=True),
    sa.Column('uploaded_at', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('url', name=u'pk_bank_transactions')
    )

def downgrade():
    op.drop_table('bank_transactions')
