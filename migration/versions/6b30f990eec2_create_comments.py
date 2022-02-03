"""create-comments

Revision ID: 6b30f990eec2
Revises: b068f4dcd4b1
Create Date: 2022-01-06 13:11:50.358502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b30f990eec2'
down_revision = 'b068f4dcd4b1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('body', sa.String, nullable=False),
    )


def downgrade():
    op.drop_table('comments')
