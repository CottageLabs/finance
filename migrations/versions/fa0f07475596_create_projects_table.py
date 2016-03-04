"""create projects table

Revision ID: fa0f07475596
Revises: 370e142881f5
Create Date: 2016-03-04 18:48:01.297273

"""

# revision identifiers, used by Alembic.
revision = 'fa0f07475596'
down_revision = '370e142881f5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('projects',
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('contact', sa.String(length=255), nullable=True),
    sa.Column('budget', sa.Integer(), nullable=True),
    sa.Column('is_ir35', sa.Boolean(), nullable=True),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.Column('budget_units', sa.String(length=255), nullable=True),
    sa.Column('normal_billing_rate', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('hours_per_day', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('uses_project_invoice_sequence', sa.Boolean(), nullable=True),
    sa.Column('currency', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('url')
    )


def downgrade():
    op.drop_table('projects')
