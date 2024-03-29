"""add log

Revision ID: 7c0c7ad663ac
Revises: c30b19286ffc
Create Date: 2022-09-07 21:25:38.412373

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7c0c7ad663ac'
down_revision = 'c30b19286ffc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('user', sa.VARCHAR(length=255), nullable=True),
    sa.Column('object', sa.VARCHAR(length=255), nullable=True),
    sa.Column('operation', sa.VARCHAR(length=255), nullable=True),
    sa.Column('result', sa.Boolean(), nullable=True),
    sa.Column('detail', sa.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_log_id'), 'log', ['id'], unique=True)
    op.create_unique_constraint('unique_timetablex_groupid', 'events', ['timetable_id', 'group_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_timetablex_groupid', 'events', type_='unique')
    op.drop_index(op.f('ix_log_id'), table_name='log')
    op.drop_table('log')
    # ### end Alembic commands ###
