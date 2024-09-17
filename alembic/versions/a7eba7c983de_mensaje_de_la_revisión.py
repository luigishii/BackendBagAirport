"""mensaje de la revisión

Revision ID: a7eba7c983de
Revises: 2f3f316cd6cb
Create Date: 2024-09-17 19:34:40.698028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7eba7c983de'
down_revision = '2f3f316cd6cb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('cpf', sa.String(), unique=True, index=True))


def downgrade():
    pass
