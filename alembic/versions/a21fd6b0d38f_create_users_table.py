"""Create users table

Revision ID: a21fd6b0d38f
Revises: 9a006e393b0a
Create Date: 2024-09-06 11:05:01.839906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a21fd6b0d38f'
down_revision = '9a006e393b0a'
branch_labels = None
depends_on = None


def upgrade():
    # Criação da tabela users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True, autoincrement=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('hashed_password', sa.String, nullable=False),
    )


def downgrade():
    op.drop_table('users')
