"""create new db

Revision ID: 09b14af95983
Revises: 1d8f87795ea0
Create Date: 2023-03-16 22:35:34.996154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09b14af95983'
down_revision = '1d8f87795ea0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('approved_types', schema=None) as batch_op:
        batch_op.alter_column('status_si',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('approved_types', schema=None) as batch_op:
        batch_op.alter_column('status_si',
               existing_type=sa.String(),
               type_=sa.BOOLEAN(),
               existing_nullable=True)

    # ### end Alembic commands ###