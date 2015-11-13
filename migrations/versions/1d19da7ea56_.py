"""empty message

Revision ID: 1d19da7ea56
Revises: None
Create Date: 2015-11-13 11:55:34.724224

"""

# revision identifiers, used by Alembic.
revision = '1d19da7ea56'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stored_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('stored_book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('holder_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['holder_id'], ['stored_user.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['stored_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stored_book')
    op.drop_table('stored_user')
    ### end Alembic commands ###