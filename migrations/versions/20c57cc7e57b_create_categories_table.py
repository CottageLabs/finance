"""create categories table

Revision ID: 20c57cc7e57b
Revises: dcf2d0a5242
Create Date: 2015-12-23 18:35:36.803473

"""

# revision identifiers, used by Alembic.
revision = '20c57cc7e57b'
down_revision = 'dcf2d0a5242'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('categories',
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('allowable_for_tax', sa.Boolean(), nullable=True),
    sa.Column('auto_sales_tax_rate', sa.String(length=255), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('group_description', sa.String(length=255), nullable=True),
    sa.Column('nominal_code', sa.String(length=255), nullable=True),
    sa.Column('tax_reporting_name', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('url')
    )


def downgrade():
    op.drop_table('categories')