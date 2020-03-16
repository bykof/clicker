"""empty message

Revision ID: 8c17c134ecd4
Revises: b8b77bef3e60
Create Date: 2020-03-13 14:24:18.177162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c17c134ecd4'
down_revision = 'b8b77bef3e60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('upgrade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cost', sa.Numeric(), nullable=True),
    sa.Column('available_at', sa.Numeric(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('upgrade_purchase',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('upgrade_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['upgrade_id'], ['upgrade.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('upgrade_purchase')
    op.drop_table('upgrade')
    # ### end Alembic commands ###
