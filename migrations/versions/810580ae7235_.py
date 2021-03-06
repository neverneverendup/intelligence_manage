"""empty message

Revision ID: 810580ae7235
Revises: 6e9600333164
Create Date: 2021-04-10 22:29:50.256704

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '810580ae7235'
down_revision = '6e9600333164'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subtask', 'user_id')
    op.add_column('user', sa.Column('subtasks', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'subtasks')
    op.add_column('subtask', sa.Column('user_id', mysql.VARCHAR(length=255), nullable=True))
    # ### end Alembic commands ###
