"""create address_id to users

Revision ID: de0a9dcc8374
Revises: 1895f3fcee05
Create Date: 2022-12-19 15:38:44.998000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de0a9dcc8374'
down_revision = '1895f3fcee05'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(),nullable=True))
    op.create_foreign_key('address_users_fk', source_table='users', referent_table='address',
                        local_cols=['address_id'], remote_cols=["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('address_users_fk', table_name='users')
    op.drop_column('address_id', table_name='users')
