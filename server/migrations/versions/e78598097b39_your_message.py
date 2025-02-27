"""your message

Revision ID: e78598097b39
Revises: 509933ab3556
Create Date: 2024-03-04 22:20:15.886088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e78598097b39'
down_revision = '509933ab3556'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('body', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'body')
    # ### end Alembic commands ###
