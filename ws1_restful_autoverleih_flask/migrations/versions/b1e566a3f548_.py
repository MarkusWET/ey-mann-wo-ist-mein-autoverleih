"""empty message

Revision ID: b1e566a3f548
Revises: 
Create Date: 2018-03-27 14:31:48.372327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1e566a3f548'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('company', sa.String(length=140), nullable=True),
    sa.Column('model', sa.String(length=140), nullable=True),
    sa.Column('price_per_day', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('loan_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('loaned_from', sa.DateTime(), nullable=True),
    sa.Column('loaned_to', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_loan_history_loaned_from'), 'loan_history', ['loaned_from'], unique=False)
    op.create_index(op.f('ix_loan_history_loaned_to'), 'loan_history', ['loaned_to'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_loan_history_loaned_to'), table_name='loan_history')
    op.drop_index(op.f('ix_loan_history_loaned_from'), table_name='loan_history')
    op.drop_table('loan_history')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('car')
    # ### end Alembic commands ###
