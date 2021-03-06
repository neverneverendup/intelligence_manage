"""empty message

Revision ID: a32946425894
Revises: d762aa28e110
Create Date: 2021-05-24 19:26:22.132588

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a32946425894'
down_revision = 'd762aa28e110'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'outside_token',
               existing_type=mysql.VARCHAR(length=255),
               type_=sa.TEXT(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'outside_token',
               existing_type=sa.TEXT(),
               type_=mysql.VARCHAR(length=255),
               existing_nullable=True)
    # ### end Alembic commands ###
