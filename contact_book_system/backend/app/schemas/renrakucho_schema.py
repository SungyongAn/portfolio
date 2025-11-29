from pydantic import BaseModel
from datetime import date, datetime


# 生徒用）連絡帳提出
class RenrakuchoEntryRequest(BaseModel):
    student_id: int
    submitted_date: date
    target_date: date
    physical_condition: int
    mental_state: int
    physical_mental_notes: str | None = None  # 追加
    daily_reflection: str


class RenrakuchoEntryResponse(BaseModel):
    success: bool
    message: str
    data: dict | None = None


# 生徒、教師共有）連絡帳検索
class PastRenrakuchoSearchRequest(BaseModel):
    # 生徒単位検索
    student_id: int | None = None

    # クラス単位検索（教師用）
    grade: int | None = None
    class_name: str | None = None
    teacher_name: str | None = None
    student_name: str | None = None

    # 共通検索条件
    year: int
    month: int
    day: int | None = None
    weekday: int | None = None
    is_read: int | None = None

    # フラグ（クラス検索か生徒検索かなどの判定用）
    flag: bool | None = None


# 生徒、教師共有）検索結果の返信
class PastRenrakuchoRecord(BaseModel):
    # 連絡帳情報
    record_date: datetime
    physical_condition: int
    mental_state: int
    physical_mental_notes: str | None = None  # 追加
    daily_reflection: str
    teacher_checked: bool
    created_at: datetime

    # 生徒情報（教師用検索時にも使える）
    student_id: int | None = None
    student_name: str | None = None


class PastRenrakuchoSearchResponse(BaseModel):
    success: bool
    message: str
    data: list[PastRenrakuchoRecord] | None = None


# 教師用）担当クラスの未チェックの連絡帳確認
class ClassNotCheckedRenrakuchoRequest(BaseModel):
    grade: int
    class_name: str


class ClassNotCheckedRenrakuchoRecord(BaseModel):
    renrakucho_id: int  # 追加（既読更新に必要）
    student_id: int
    student_name: str
    record_date: date
    physical_condition: int | None = None
    mental_state: int | None = None
    physical_mental_notes: str | None = None  # 追加
    daily_reflection: str | None = None
    teacher_checked: bool
    submitted_date: datetime | None = None
    created_at: datetime | None = None


class ClassNotCheckedRenrakuchoResponse(BaseModel):
    success: bool
    message: str | None = None
    data: list[ClassNotCheckedRenrakuchoRecord] | None = None


# 教師用）連絡帳の既読更新
class MarkAsReadRequest(BaseModel):
    renrakucho_ids: list[int]


class MarkAsReadResponse(BaseModel):
    success: bool
    message: str | None = None
    data: dict | None = None  # 追加


# 提出状況確認リクエスト
class SubmissionStatusRequest(BaseModel):
    grade: int
    class_name: str
    target_date: date


# 提出状況レスポンス
class SubmissionStatusResponse(BaseModel):
    success: bool
    message: str | None = None
    data: dict | None = None


# 養護教諭用）要注意連絡帳の取得
class CriticalEntryRecord(BaseModel):
    renrakucho_id: int
    student_id: int
    student_name: str
    grade: int
    class_name: str
    submitted_date: str
    target_date: str
    physical_condition: int
    mental_state: int
    physical_mental_notes: str | None = None
    created_at: str | None = None


class CriticalEntriesResponse(BaseModel):
    success: bool
    message: str
    data: list[CriticalEntryRecord] | None = None
