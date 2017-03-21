"""create server_costs table

Revision ID: 1e27c434bb14
Revises: fa0f07475596
Create Date: 2016-03-14 15:57:19.945327

"""

# revision identifiers, used by Alembic.
revision = '1e27c434bb14'
down_revision = 'fa0f07475596'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table(
        'server_costs',
        sa.Column('project_url', sa.String(length=255), sa.ForeignKey('projects.url'), nullable=False, primary_key=True),
        sa.Column('value', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_table('server_costs')
