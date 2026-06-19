from datetime import date

from app.models.project import Project
from app.models.task import Task


def to_status_value(status) -> str:
    """Enum / str のどちらでも比較しやすいように文字列化する"""
    return status.value if hasattr(status, "value") else str(status)


def calc_consumption_rate(
    budget_amount: int | None,
    actual_amount: int | None,
) -> int:
    """予算消費率を算出"""
    if not budget_amount or budget_amount <= 0:
        return 0

    actual = actual_amount or 0
    return round((actual / budget_amount) * 100)


def calc_project_progress(tasks: list[Task]) -> int:
    """タスク進捗率から案件進捗率を算出"""
    if not tasks:
        return 0

    return round(sum(task.progress for task in tasks) / len(tasks))


def calc_schedule_rate(project: Project) -> int:
    """案件期間に対する予定進捗率を算出"""
    if not project.start_date or not project.end_date:
        return 0

    start = (
        project.start_date.date()
        if hasattr(project.start_date, "date")
        else project.start_date
    )
    end = (
        project.end_date.date()
        if hasattr(project.end_date, "date")
        else project.end_date
    )

    today = date.today()

    if today <= start:
        return 0

    if today >= end:
        return 100

    total_days = (end - start).days
    passed_days = (today - start).days

    if total_days <= 0:
        return 100

    return round((passed_days / total_days) * 100)


def judge_alert(
    progress: int,
    schedule_rate: int,
    consumption_rate: int,
    overdue_task_count: int,
) -> dict:
    reasons = []

    schedule_diff = progress - schedule_rate
    consumption_diff = progress - consumption_rate

    if progress == 0 and schedule_rate >= 20:
        reasons.append("未着手")

    if schedule_diff <= -20:
        reasons.append("納期遅延")

    if consumption_diff <= -25:
        reasons.append("予算超過")

    if overdue_task_count > 0:
        reasons.append("期限超過")

    level = None

    if schedule_diff <= -20 or consumption_diff <= -25:
        level = "danger"

    elif schedule_diff <= -10 or consumption_diff <= -15 or overdue_task_count > 0:
        level = "warning"

    return {
        "level": level,
        "reason": " + ".join(reasons) if reasons else None,
    }


def calc_spi(progress: int, schedule_rate: int) -> float | None:
    """SPI: 予定進捗に対する実績進捗"""
    if schedule_rate <= 0:
        return None

    return round(progress / schedule_rate, 2)


def calc_cpi(progress: int, consumption_rate: int) -> float | None:
    """CPI: 予算消費率に対する実績進捗"""
    if consumption_rate <= 0:
        return None

    return round(progress / consumption_rate, 2)
