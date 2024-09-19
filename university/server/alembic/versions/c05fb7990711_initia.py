"""initia

Revision ID: c05fb7990711
Revises: bb9419289da9
Create Date: 2024-09-19 10:41:14.956688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c05fb7990711'
down_revision: Union[str, None] = 'bb9419289da9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('professors',
    sa.Column('id_professor', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('department_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['department_name'], ['department.name'], ),
    sa.PrimaryKeyConstraint('id_professor')
    )
    op.create_index(op.f('ix_professors_name'), 'professors', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_professors_name'), table_name='professors')
    op.drop_table('professors')
    # ### end Alembic commands ###
