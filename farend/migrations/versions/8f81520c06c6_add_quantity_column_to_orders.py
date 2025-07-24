"""Add quantity column to orders

Revision ID: 8f81520c06c6
Revises: a8c5a09634e9
Create Date: 2025-07-21 20:20:49.879237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f81520c06c6'
down_revision = 'a8c5a09634e9'
branch_labels = None
depends_on = None


def upgrade():
    # Add quantity column with default for existing rows
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('quantity', sa.Integer(), nullable=False, server_default='1'))
        batch_op.alter_column('status',
            existing_type=sa.VARCHAR(length=20),
            nullable=False)

    # Remove the server default to keep future inserts explicit
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('quantity', server_default=None)


def downgrade():
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('status',
            existing_type=sa.VARCHAR(length=20),
            nullable=True)
        batch_op.drop_column('quantity')
