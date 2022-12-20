"""create phone number col for user

Revision ID: 6f135b91eb9c
Revises: 
Create Date: 2022-12-19 15:17:05.201487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f135b91eb9c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable = True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
