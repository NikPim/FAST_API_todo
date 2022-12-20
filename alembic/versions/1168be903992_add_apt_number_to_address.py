"""add apt number to address

Revision ID: 1168be903992
Revises: de0a9dcc8374
Create Date: 2022-12-20 13:04:17.105970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1168be903992'
down_revision = 'de0a9dcc8374'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt_num', sa.Integer(),nullable=True))


def downgrade() -> None:
    op.drop_column('apt_num', table_name='address')
