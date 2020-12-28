"""empty message

Revision ID: 259646109f82
Revises: c8d49439a7a1
Create Date: 2020-12-28 11:34:59.709731

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '259646109f82'
down_revision = 'c8d49439a7a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('score_data', sa.Column('create_time', sa.DateTime(), nullable=True))
    op.drop_column('score_data', 'crate_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('score_data', sa.Column('crate_time', mysql.DATETIME(), nullable=True))
    op.drop_column('score_data', 'create_time')
    # ### end Alembic commands ###