"""bugfix primarykey on authority

Revision ID: b34314807351
Revises: 8d30073e58f8
Create Date: 2022-08-14 20:58:07.066473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b34314807351'
down_revision = '8d30073e58f8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authority', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.create_unique_constraint(None, 'authority', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'authority', type_='unique')
    op.drop_column('authority', 'id')
    # ### end Alembic commands ###
