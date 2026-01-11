"""add_assignments_and_submissions

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2026-01-09 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'b2c3d4e5f6g7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'assignment',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('module_name', sa.String(length=255), nullable=True),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'submission',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('assignment_id', sa.Integer(), sa.ForeignKey('assignment.id'), nullable=False, index=True),
        sa.Column('student_id', sa.String(length=36), sa.ForeignKey('user.id'), nullable=True, index=True),
        sa.Column('content_url', sa.String(length=2048), nullable=True),
        sa.Column('content_text', sa.Text(), nullable=True),
        sa.Column('grade', sa.Integer(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade():
    op.drop_table('submission')
    op.drop_table('assignment')
