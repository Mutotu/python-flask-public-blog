"""create-topics

Revision ID: eb318d4b66ca
Revises: bae29571740d
Create Date: 2022-01-06 13:24:29.340374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb318d4b66ca'
down_revision = 'bae29571740d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'topics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False)
    )


def downgrade():
    op.drop_table('topics')
