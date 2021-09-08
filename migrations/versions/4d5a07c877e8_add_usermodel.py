"""Add UserModel

Revision ID: 4d5a07c877e8
Revises: 
Create Date: 2021-09-07 21:07:09.702272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d5a07c877e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('author_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('surname', sa.String(length=32), server_default='Unknown', nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_model_username'), 'user_model', ['username'], unique=False)
    op.create_table('quote_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('quote', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author_model.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quote_model')
    op.drop_index(op.f('ix_user_model_username'), table_name='user_model')
    op.drop_table('user_model')
    op.drop_table('author_model')
    # ### end Alembic commands ###