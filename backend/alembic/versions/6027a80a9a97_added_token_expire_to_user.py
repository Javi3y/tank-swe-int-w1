"""added token expire to user

Revision ID: 6027a80a9a97
Revises: 195dbf46f85d
Create Date: 2025-01-29 15:38:19.138457

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6027a80a9a97"
down_revision: Union[str, None] = "195dbf46f85d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("token_expire", sa.DateTime(timezone=True), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "token_expire")
    # ### end Alembic commands ###
