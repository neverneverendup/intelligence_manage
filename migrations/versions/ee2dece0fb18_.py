"""empty message

Revision ID: ee2dece0fb18
Revises: 353becc4e388
Create Date: 2021-04-07 10:50:55.452047

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ee2dece0fb18'
down_revision = '353becc4e388'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subtask', 'itemCount',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('subtask', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subtask', 'name',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('subtask', 'itemCount',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    # ### end Alembic commands ###
