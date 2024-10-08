"""Initial migration.

Revision ID: v1.0
Revises: 
Create Date: 2024-08-28 00:00:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1.0'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create QueryLog table
    op.create_table(
        'query_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('domain', sa.String(length=255), nullable=False),
        sa.Column('result', sa.String(length=1024), nullable=False),
        sa.Column('timestamp', sa.DateTime, default=sa.func.now(), nullable=False),
    )

def downgrade():
    # Drop QueryLog table
    op.drop_table('query_log')
