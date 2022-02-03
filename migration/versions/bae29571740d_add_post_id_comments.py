"""add-post-id-comments

Revision ID: bae29571740d
Revises: 6b30f990eec2
Create Date: 2022-01-06 13:18:59.454466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bae29571740d'
down_revision = '6b30f990eec2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('comments', sa.Column('post_id', sa.Integer))


def downgrade():
    op.remove_column('comments','post_id')
