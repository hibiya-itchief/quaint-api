"""hebe

Revision ID: 278ab09027c9
Revises: e6f6f1366a60
Create Date: 2023-09-14 01:27:10.589980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '278ab09027c9'
down_revision = 'e6f6f1366a60'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hebenowplaying',
    sa.Column('group_id', sa.VARCHAR(length=255), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('group_id')
    )
    op.create_index(op.f('ix_hebenowplaying_group_id'), 'hebenowplaying', ['group_id'], unique=False)
    op.create_table('hebeupnext',
    sa.Column('group_id', sa.VARCHAR(length=255), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('group_id')
    )
    op.create_index(op.f('ix_hebeupnext_group_id'), 'hebeupnext', ['group_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_hebeupnext_group_id'), table_name='hebeupnext')
    op.drop_table('hebeupnext')
    op.drop_index(op.f('ix_hebenowplaying_group_id'), table_name='hebenowplaying')
    op.drop_table('hebenowplaying')
    # ### end Alembic commands ###
