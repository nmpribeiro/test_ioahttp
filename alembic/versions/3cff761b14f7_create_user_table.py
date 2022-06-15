"""create user table

Revision ID: 3cff761b14f7
Revises: 
Create Date: 2022-06-15 15:15:33.977026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cff761b14f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    import enum

    class Gender(enum.Enum):
        female = 'female'
        male = 'male'
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        # sa.Column('description', sa.Unicode(200)),
        sa.Column('user_id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(256), nullable=False, unique=True),
        sa.Column('name', sa.String(collation='ru-RU-x-icu'), nullable=False),
        sa.Column('gender', sa.Enum(Gender, name='gender'), nullable=False),
        sa.Column('floor', sa.SmallInteger, nullable=False),
        sa.Column('seat', sa.SmallInteger, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('users')
