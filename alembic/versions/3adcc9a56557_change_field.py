revision = '3adcc9a56557'
down_revision = None
branch_labels = None


from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date


def upgrade():
    op.add_column('Ticket', Column('seat', Integer))


def downgrade():
    op.drop_column('Ticket', 'seat')
