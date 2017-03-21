"""drop server costs foreign key to projects

Revision ID: 3b288c733c84
Revises: 423a0156bbac
Create Date: 2016-03-17 11:01:35.523203

"""

# revision identifiers, used by Alembic.
revision = '3b288c733c84'
down_revision = '423a0156bbac'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint('server_costs_project_url_fkey', 'server_costs')


def downgrade():
    op.create_foreign_key(
        'server_costs_project_url_fkey',
        source='server_costs',
        referent='projects',
        local_cols=['project_url'],
        remote_cols=['url']
    )
