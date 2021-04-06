"""'修改demand为BLOB类型'

Revision ID: 06bbcd9900cb
Revises: 56d5e2fdc691
Create Date: 2021-03-26 17:25:35.859856

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '06bbcd9900cb'
down_revision = '56d5e2fdc691'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'demand',
               existing_type=mysql.TEXT(),
               type_=sa.BLOB(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('task', 'demand',
               existing_type=sa.BLOB(),
               type_=mysql.TEXT(),
               existing_nullable=True)
    # ### end Alembic commands ###
