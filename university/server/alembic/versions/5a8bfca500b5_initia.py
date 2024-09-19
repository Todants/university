"""initia

Revision ID: 5a8bfca500b5
Revises: 7987fb3ec812
Create Date: 2024-09-19 10:25:47.262101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a8bfca500b5'
down_revision: Union[str, None] = '7987fb3ec812'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('group',
    sa.Column('id_group', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id_group', 'name')
    )
    op.create_table('instructor',
    sa.Column('id_instructor', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.Column('employ_date', sa.DateTime(), nullable=True),
    sa.Column('photo', sa.LargeBinary(), nullable=True),
    sa.Column('department_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['department_name'], ['department.name'], ),
    sa.PrimaryKeyConstraint('id_instructor')
    )
    op.create_table('student',
    sa.Column('id_student', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.Column('enroll_date', sa.DateTime(), nullable=True),
    sa.Column('photo', sa.LargeBinary(), nullable=True),
    sa.Column('group_name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['group_name'], ['group.name'], ),
    sa.PrimaryKeyConstraint('id_student')
    )
    op.create_table('subject',
    sa.Column('id_subject', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id_student'], ),
    sa.PrimaryKeyConstraint('id_subject')
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
