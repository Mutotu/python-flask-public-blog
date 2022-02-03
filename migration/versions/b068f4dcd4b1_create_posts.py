"""create-posts

Revision ID: b068f4dcd4b1
Revises: 
Create Date: 2022-01-06 13:07:35.817670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b068f4dcd4b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('body', sa.String, nullable=False)
    )


def downgrade():
    op.drop_table('posts')
