"""removed default time for subscription end

Revision ID: 13969595b031
Revises: d3c3f0eb6761
Create Date: 2025-01-28 23:13:18.890052

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "13969595b031"
down_revision: Union[str, None] = "d3c3f0eb6761"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
