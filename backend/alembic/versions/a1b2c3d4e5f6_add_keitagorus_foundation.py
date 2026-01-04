\"\"\"add_keitagorus_foundation

Revision ID: a1b2c3d4e5f6
Revises: 
Create Date: 2026-01-04 00:00:00.000000

\"\"\"
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'user_file',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('owner_id', sa.String(), nullable=False),
        sa.Column('original_filename', sa.String(), nullable=False),
        sa.Column('stored_path', sa.String(), nullable=False),
        sa.Column('content_type', sa.String(), nullable=True),
        sa.Column('size', sa.BigInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'student_progress',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('lesson_id', sa.String(), nullable=True),
        sa.Column('progress_percentage', sa.Integer(), nullable=False, server_default="0"),
        sa.Column('last_score', sa.Float(), nullable=True),
        sa.Column('attempts', sa.Integer(), nullable=False, server_default="0"),
        sa.Column('struggling', sa.Boolean(), nullable=False, server_default="false"),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    # Add ar_model_url to lesson/item if exists
    # op.add_column('item', sa.Column('ar_model_url', sa.String(length=2048), nullable=True))

def downgrade():
    # op.drop_column('item', 'ar_model_url')
    op.drop_table('student_progress')
    op.drop_table('user_file')
