"""empty message

Revision ID: 86dab0281639
Revises: 83fa5d65327f
Create Date: 2020-12-21 16:39:18.915497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86dab0281639'
down_revision = '83fa5d65327f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('score_data',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('score1', sa.Integer(), nullable=False),
    sa.Column('score2', sa.Integer(), nullable=False),
    sa.Column('score3', sa.Integer(), nullable=False),
    sa.Column('suggest', sa.Text(), nullable=True),
    sa.Column('crate_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('score_data')
    # ### end Alembic commands ###
