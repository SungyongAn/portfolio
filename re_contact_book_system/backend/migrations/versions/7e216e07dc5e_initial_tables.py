from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


revision = "xxxx_initial_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum("student", "teacher", "admin"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ),
        sa.UniqueConstraint("email"),
        sa.Index("idx_email", "email"),
        sa.Index("idx_role", "role"),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_unicode_ci",
    )

    # grades
    op.create_table(
        "grades",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("grade_number", sa.Integer, nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("grade_number", "year", name="uk_grade_year"),
        sa.Index("idx_year", "year"),
    )

    # classes
    op.create_table(
        "classes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("grade_id", sa.Integer, sa.ForeignKey("grades.id", ondelete="CASCADE")),
        sa.Column("class_name", sa.String(50), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("grade_id", "class_name", name="uk_grade_class"),
        sa.Index("idx_grade_id", "grade_id"),
    )

    # student_class_assignments
    op.create_table(
        "student_class_assignments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("class_id", sa.Integer, sa.ForeignKey("classes.id", ondelete="CASCADE")),
        sa.Column("is_current", sa.Boolean, server_default=sa.true()),
        sa.Column("assigned_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Index("idx_student_id", "student_id"),
        sa.Index("idx_class_id", "class_id"),
        sa.Index("idx_is_current", "is_current"),
    )

    # teacher_assignments
    op.create_table(
        "teacher_assignments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("teacher_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column(
            "assignment_type",
            sa.Enum("homeroom", "subject", "grade_head", "administrator"),
            nullable=False,
        ),
        sa.Column("grade_id", sa.Integer, sa.ForeignKey("grades.id", ondelete="CASCADE")),
        sa.Column("class_id", sa.Integer, sa.ForeignKey("classes.id", ondelete="CASCADE")),
        sa.Column("subject_name", sa.String(50)),
        sa.Column("is_primary", sa.Boolean, server_default=sa.false()),
        sa.Column(
            "permission_level",
            sa.Enum("read", "write", "admin"),
            server_default="read",
        ),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Index("idx_teacher_id", "teacher_id"),
        sa.Index("idx_assignment_type", "assignment_type"),
        sa.Index("idx_class_id", "class_id"),
        sa.Index("idx_grade_id", "grade_id"),
    )

    # journal_entries
    op.create_table(
        "journal_entries",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("entry_date", sa.Date, nullable=False),
        sa.Column("submission_date", sa.Date, nullable=False),
        sa.Column("physical_condition", sa.String(50), nullable=False),
        sa.Column("mental_condition", sa.String(50), nullable=False),
        sa.Column("reflection_text", sa.Text),
        sa.Column("is_read", sa.Boolean, server_default=sa.false()),
        sa.Column("read_by", sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("read_at", sa.TIMESTAMP),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ),
        sa.Index("idx_student_id", "student_id"),
        sa.Index("idx_entry_date", "entry_date"),
        sa.Index("idx_submission_date", "submission_date"),
        sa.Index("idx_is_read", "is_read"),
        sa.Index("idx_read_by", "read_by"),
    )

    # teacher_notes
    op.create_table(
        "teacher_notes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("teacher_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("student_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column(
            "entry_id",
            sa.Integer,
            sa.ForeignKey("journal_entries.id", ondelete="SET NULL"),
        ),
        sa.Column("note_text", sa.Text, nullable=False),
        sa.Column("is_shared", sa.Boolean, server_default=sa.false()),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP,
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ),
        sa.Index("idx_teacher_id", "teacher_id"),
        sa.Index("idx_student_id", "student_id"),
        sa.Index("idx_entry_id", "entry_id"),
        sa.Index("idx_is_shared", "is_shared"),
        sa.Index("idx_created_at", "created_at"),
    )


def downgrade():
    op.drop_table("teacher_notes")
    op.drop_table("journal_entries")
    op.drop_table("teacher_assignments")
    op.drop_table("student_class_assignments")
    op.drop_table("classes")
    op.drop_table("grades")
    op.drop_table("users")
