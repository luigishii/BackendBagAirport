"""Create users table

Revision ID: 2f3f316cd6cb
Revises: a21fd6b0d38f
Create Date: 2024-09-06 11:06:12.284265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f3f316cd6cb'
down_revision = 'a21fd6b0d38f'
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

