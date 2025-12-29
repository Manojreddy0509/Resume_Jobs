"""merge heads

Revision ID: d8f13af35751
Revises: 0002_create_matches_table, d03502623932
Create Date: 2025-12-25 18:36:38.743620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8f13af35751'
down_revision = ('0002_create_matches_table', 'd03502623932')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
