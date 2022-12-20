"""create address table

Revision ID: 1895f3fcee05
Revises: 6f135b91eb9c
Create Date: 2022-12-19 15:32:22.076082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1895f3fcee05'
down_revision = '6f135b91eb9c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('address',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.String, nullable = False),
                    sa.Column('address2', sa.String, nullable = False),
                    sa.Column('city', sa.String, nullable = False),
                    sa.Column('state', sa.String, nullable = False),
                    sa.Column('country', sa.String, nullable = False),
                    sa.Column('postalcode', sa.String, nullable = False)
    )


def downgrade() -> None:
    op.drop_table('address')
