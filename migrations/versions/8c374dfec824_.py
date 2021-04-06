"""empty message

Revision ID: 8c374dfec824
Revises: c35b52de1475
Create Date: 2021-04-04 20:53:56.663843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c374dfec824'
down_revision = 'c35b52de1475'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('createTime', sa.DateTime(), nullable=True))
    op.add_column('task', sa.Column('subtaskDemand', sa.Integer(), nullable=True))
    op.add_column('task', sa.Column('teamDemand', sa.String(length=255), nullable=True))
    op.add_column('task', sa.Column('timeDemand', sa.DateTime(), nullable=True))
    op.drop_column('task', 'demand')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('demand', sa.BLOB(), nullable=True))
    op.drop_column('task', 'timeDemand')
    op.drop_column('task', 'teamDemand')
    op.drop_column('task', 'subtaskDemand')
    op.drop_column('task', 'createTime')
    # ### end Alembic commands ###