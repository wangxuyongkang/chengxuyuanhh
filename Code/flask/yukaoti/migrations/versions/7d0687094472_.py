"""empty message

Revision ID: 7d0687094472
Revises: 
Create Date: 2019-06-24 15:32:11.935204

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7d0687094472'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hero', sa.Column('image', sa.String(length=100), nullable=False))
    op.alter_column('hero', 'name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.drop_column('hero', 'url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hero', sa.Column('url', mysql.VARCHAR(length=255), nullable=True))
    op.alter_column('hero', 'name',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.drop_column('hero', 'image')
    # ### end Alembic commands ###
