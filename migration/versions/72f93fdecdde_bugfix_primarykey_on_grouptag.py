"""bugfix primarykey on grouptag

Revision ID: 72f93fdecdde
Revises: b34314807351
Create Date: 2022-08-14 21:38:30.562572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72f93fdecdde'
down_revision = 'b34314807351'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('grouptag', sa.Column('id', sa.Integer(), autoincrement=True, nullable=False))
    op.create_unique_constraint(None, 'grouptag', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'grouptag', type_='unique')
    op.drop_column('grouptag', 'id')
    # ### end Alembic commands ###
