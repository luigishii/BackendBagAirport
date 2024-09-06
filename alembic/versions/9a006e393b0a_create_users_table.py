"""Create users table

Revision ID: 9a006e393b0a
Revises: 0dcf1481aed6
Create Date: 2024-09-06 11:02:18.643470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a006e393b0a'
down_revision = '0dcf1481aed6'
branch_labels = None
depends_on = None


def upgrade():
    # Criação da tabela users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True, autoincrement=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('full_name', sa.String, nullable=True),
        sa.Column('hashed_password', sa.String, nullable=False),
    )


def downgrade():
    op.drop_table('users')
