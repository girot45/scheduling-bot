"""New table User

Revision ID: dec050ee31f5
Revises: c2cee86db506
Create Date: 2023-11-18 01:08:41.622072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dec050ee31f5'
down_revision: Union[str, None] = 'c2cee86db506'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Table', 'isrepeat',
               existing_type=sa.INTEGER(),
               server_default='0',
               existing_nullable=False)
    op.alter_column('User', 'need_notif',
               existing_type=sa.INTEGER(),
               server_default='1',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('User', 'need_notif',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=True)
    op.alter_column('Table', 'isrepeat',
               existing_type=sa.INTEGER(),
               server_default=None,
               existing_nullable=False)
    # ### end Alembic commands ###
