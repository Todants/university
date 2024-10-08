"""ini

Revision ID: 9c6bbcef9f42
Revises: 6c617dc859ec
Create Date: 2024-09-26 11:45:15.965305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c6bbcef9f42'
down_revision = '6c617dc859ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('professor_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'group', 'professors', ['professor_id'], ['id_professor'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'group', type_='foreignkey')
    op.drop_column('group', 'professor_id')
    # ### end Alembic commands ###
