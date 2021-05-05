"""empty message

Revision ID: bdb6a0b36ccd
Revises: b2fc53842894
Create Date: 2021-05-05 19:50:25.658058

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bdb6a0b36ccd'
down_revision = 'b2fc53842894'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('inside_token', sa.String(length=255), nullable=True))
    op.add_column('user', sa.Column('outside_token', sa.String(length=255), nullable=True))
    op.drop_index('token', table_name='user')
    op.create_unique_constraint(None, 'user', ['inside_token'])
    op.create_unique_constraint(None, 'user', ['outside_token'])
    op.drop_column('user', 'token')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token', mysql.VARCHAR(length=255), nullable=False))
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.create_index('token', 'user', ['token'], unique=True)
    op.drop_column('user', 'outside_token')
    op.drop_column('user', 'inside_token')
    # ### end Alembic commands ###
