"""Initial migration

Revision ID: d0b02d2752dd
Revises: 
Create Date: 2024-09-17 00:18:33.304098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0b02d2752dd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('group',
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('instructor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.Column('employ_date', sa.DateTime(), nullable=True),
    sa.Column('photo', sa.BLOB(), nullable=True),
    sa.Column('department_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['department_name'], ['department.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.Column('enroll_date', sa.DateTime(), nullable=True),
    sa.Column('photo', sa.BLOB(), nullable=True),
    sa.Column('group_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['group_name'], ['group.name'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subject',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subject')
    op.drop_table('student')
    op.drop_table('instructor')
    op.drop_table('group')
    op.drop_table('department')
    # ### end Alembic commands ###