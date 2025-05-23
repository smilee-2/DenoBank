"""2 mig

Revision ID: f586a4f056f6
Revises: 432d99426982
Create Date: 2025-04-27 17:17:26.137540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f586a4f056f6'
down_revision: Union[str, None] = '432d99426982'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('payments_score_id_key', 'payments', type_='unique')
    op.create_unique_constraint(None, 'scores', ['score_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'scores', type_='unique')
    op.create_unique_constraint('payments_score_id_key', 'payments', ['score_id'])
    # ### end Alembic commands ###
