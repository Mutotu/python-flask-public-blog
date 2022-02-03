"""create-taggings

Revision ID: 578324f9d4d3
Revises: eb318d4b66ca
Create Date: 2022-01-06 13:26:36.580547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '578324f9d4d3'
down_revision = 'eb318d4b66ca'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'taggings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('post_id', sa.Integer),
        sa.Column('topic_id', sa.Integer)
    )


def downgrade():
    op.drop_table('taggings')
