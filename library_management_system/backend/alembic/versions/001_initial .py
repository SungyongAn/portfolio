"""initial_schema

Revision ID: 78f473ec6f81
Revises:
Create Date: 2026-04-10

全テーブルの初期作成マイグレーション。
テーブル作成順序は外部キー制約を考慮した依存順。
"""
from alembic import op
import sqlalchemy as sa

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── schools ──────────────────────────────────────────────────────
    op.create_table(
        "schools",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False, comment="学校名"),
        sa.Column("code", sa.String(length=10), nullable=False, comment="学校コード (A〜E)"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )

    # ── users ────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("school_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, comment="学校メールアドレス"),
        sa.Column("password_hash", sa.String(length=255), nullable=False, comment="Argon2ハッシュ"),
        sa.Column("name", sa.String(length=100), nullable=False, comment="氏名"),
        sa.Column("barcode", sa.String(length=50), nullable=True, comment="図書館カードバーコード"),
        sa.Column("grade", sa.Integer(), nullable=True, comment="学年 (1〜3)"),
        sa.Column("class_name", sa.String(length=20), nullable=True, comment="クラス名"),
        sa.Column("role", sa.Enum("student", "librarian", "admin", name="user_role"), nullable=False),
        sa.Column("is_committee", sa.Boolean(), nullable=False, comment="図書委員フラグ"),
        sa.Column("is_active", sa.Boolean(), nullable=False, comment="退学・卒業フラグ"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("barcode"),
    )
    op.create_index("ix_users_school_id", "users", ["school_id"])
    op.create_index("ix_users_role", "users", ["role"])

    # ── password_reset_tokens ────────────────────────────────────────
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False, comment="SHA-256ハッシュ済みトークン"),
        sa.Column("expires_at", sa.DateTime(), nullable=False, comment="有効期限 (発行から30分)"),
        sa.Column("used_at", sa.DateTime(), nullable=True, comment="使用日時（1回使い捨て）"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index("ix_password_reset_tokens_user_id", "password_reset_tokens", ["user_id"])

    # ── books ────────────────────────────────────────────────────────
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("school_id", sa.Integer(), nullable=False, comment="所蔵学校"),
        sa.Column("barcode", sa.String(length=50), nullable=False, comment="資料バーコード (統一採番)"),
        sa.Column("isbn", sa.String(length=20), nullable=True, comment="ISBN-13"),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=True),
        sa.Column("publisher", sa.String(length=255), nullable=True),
        sa.Column("published_year", sa.Integer(), nullable=True),
        sa.Column("ndc", sa.String(length=10), nullable=True, comment="日本十進分類法コード"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("available", "reserved", "on_loan", "inter_library", "discarded", name="book_status"),
            nullable=False,
        ),
        sa.Column("discarded_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["school_id"], ["schools.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("barcode"),
    )
    op.create_index("ix_books_school_id", "books", ["school_id"])
    op.create_index("ix_books_isbn", "books", ["isbn"])
    op.create_index("ix_books_status", "books", ["status"])
    op.create_index("ix_books_ndc", "books", ["ndc"])

    # ── loans ────────────────────────────────────────────────────────
    op.create_table(
        "loans",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("loaned_by", sa.Integer(), nullable=True, comment="代理貸出操作者 (司書/図書委員)"),
        sa.Column("loaned_at", sa.DateTime(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False, comment="返却期限"),
        sa.Column("returned_at", sa.DateTime(), nullable=True),
        sa.Column("returned_by", sa.Integer(), nullable=True, comment="代理返却操作者"),
        sa.Column("extended_count", sa.Integer(), nullable=False, comment="延長回数 (UC-28 / 課題2で確定予定)"),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"]),
        sa.ForeignKeyConstraint(["loaned_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["returned_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_loans_user_id", "loans", ["user_id"])
    op.create_index("ix_loans_book_id", "loans", ["book_id"])
    op.create_index("ix_loans_due_date", "loans", ["due_date"])
    op.create_index("ix_loans_returned_at", "loans", ["returned_at"])

    # ── reservations ─────────────────────────────────────────────────
    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("reserved_by", sa.Integer(), nullable=True, comment="代理予約操作者"),
        sa.Column(
            "status",
            sa.Enum("waiting", "ready", "canceled", "expired", "fulfilled", name="reservation_status"),
            nullable=False,
        ),
        sa.Column("notified_at", sa.DateTime(), nullable=True, comment="準備完了通知日時"),
        sa.Column("ready_deadline", sa.DateTime(), nullable=True, comment="取置き期限"),
        sa.Column("canceled_at", sa.DateTime(), nullable=True),
        sa.Column("fulfilled_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"]),
        sa.ForeignKeyConstraint(["reserved_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reservations_user_id", "reservations", ["user_id"])
    op.create_index("ix_reservations_book_id", "reservations", ["book_id"])
    op.create_index("ix_reservations_status", "reservations", ["status"])

    # ── inter_library_requests ───────────────────────────────────────
    op.create_table(
        "inter_library_requests",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False, comment="申請者"),
        sa.Column("book_id", sa.Integer(), nullable=False, comment="対象資料（他校蔵書）"),
        sa.Column("requested_by", sa.Integer(), nullable=True, comment="代理申請者"),
        sa.Column("from_school_id", sa.Integer(), nullable=False, comment="貸出元学校"),
        sa.Column("to_school_id", sa.Integer(), nullable=False, comment="届け先学校"),
        sa.Column(
            "status",
            sa.Enum("pending", "confirmed", "shipped", "arrived", "fulfilled", "canceled", name="inter_library_status"),
            nullable=False,
        ),
        sa.Column("deadline", sa.DateTime(), nullable=True, comment="締め切り日時（金曜15時）"),
        sa.Column("shipped_at", sa.DateTime(), nullable=True, comment="発送登録日時"),
        sa.Column("arrived_at", sa.DateTime(), nullable=True, comment="着荷登録日時"),
        sa.Column("notified_at", sa.DateTime(), nullable=True, comment="着荷通知日時"),
        sa.Column("canceled_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"]),
        sa.ForeignKeyConstraint(["from_school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["requested_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["to_school_id"], ["schools.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_inter_library_requests_user_id", "inter_library_requests", ["user_id"])
    op.create_index("ix_inter_library_requests_book_id", "inter_library_requests", ["book_id"])
    op.create_index("ix_inter_library_requests_status", "inter_library_requests", ["status"])
    op.create_index("ix_inter_library_requests_from_school", "inter_library_requests", ["from_school_id"])
    op.create_index("ix_inter_library_requests_to_school", "inter_library_requests", ["to_school_id"])


def downgrade() -> None:
    op.drop_table("inter_library_requests")
    op.drop_table("reservations")
    op.drop_table("loans")
    op.drop_table("books")
    op.drop_table("password_reset_tokens")
    op.drop_table("users")
    op.drop_table("schools")
    sa.Enum(name="inter_library_status").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="reservation_status").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="book_status").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="user_role").drop(op.get_bind(), checkfirst=True)