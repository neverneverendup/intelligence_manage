"""empty message

Revision ID: ff3f95c1f0c4
Revises: 44bafb51c274
Create Date: 2021-05-24 17:34:44.297584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff3f95c1f0c4'
down_revision = '44bafb51c274'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subtask', sa.Column('user_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subtask', 'user_id')
    # ### end Alembic commands ###
