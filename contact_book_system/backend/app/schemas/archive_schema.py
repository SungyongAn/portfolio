from pydantic import BaseModel, Field
from datetime import date, datetime


class ArchiveStatisticsResponse(BaseModel):
    """アーカイブ統計レスポンス"""
    data_type: str = Field(..., description="データタイプ（active/archive）")
    record_count: int = Field(..., description="レコード数")
    oldest_date: date | None = Field(default=None, description="最古の日付")
    newest_date: date | None = Field(default=None, description="最新の日付")
    size_mb: float = Field(..., description="サイズ（MB）")


class ArchiveExecutionRequest(BaseModel):
    """アーカイブ実行リクエスト"""
    archive_years: int | None = Field(
        default=3,
        ge=1,
        le=10,
        description="何年前のデータをアーカイブするか"
    )


class DeleteExecutionRequest(BaseModel):
    """削除実行リクエスト"""
    retention_years: int | None = Field(
        default=5,
        ge=1,
        le=20,
        description="何年間データを保持するか"
    )


class ArchiveExecutionResponse(BaseModel):
    """アーカイブ実行レスポンス"""
    success: bool
    message: str
    records_archived: int
    cutoff_date: date


class DeleteExecutionResponse(BaseModel):
    """削除実行レスポンス"""
    success: bool
    message: str
    records_deleted: int
    cutoff_date: date
    backup_file: str | None = None


class DeletionLogResponse(BaseModel):
    """削除ログレスポンス"""
    id: int
    deletion_date: datetime
    table_name: str
    records_deleted: int
    date_range_from: date | None = None
    date_range_to: date | None = None
    reason: str | None = None
    executed_by: str
    backup_file: str | None = None
