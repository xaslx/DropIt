"""empty message

Revision ID: 3ee1bae41747
Revises: 16fead08bce2
Create Date: 2024-09-16 12:41:31.243096

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ee1bae41747'
down_revision: Union[str, None] = '16fead08bce2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blacklist', sa.Column('id', sa.Integer(), nullable=False))
    op.create_unique_constraint(None, 'blacklist', ['ip_address'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'blacklist', type_='unique')
    op.drop_column('blacklist', 'id')
    # ### end Alembic commands ###
