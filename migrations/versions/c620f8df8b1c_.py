"""empty message

Revision ID: c620f8df8b1c
Revises: b609e3b2d629
Create Date: 2016-11-07 14:43:09.463287

"""

# revision identifiers, used by Alembic.
revision = 'c620f8df8b1c'
down_revision = 'b609e3b2d629'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('citations', sa.Column('text_content_vector_rep', postgresql.ARRAY(sa.Float()), server_default='{}', nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('citations', 'text_content_vector_rep')
    ### end Alembic commands ###
