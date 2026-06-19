from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.task import Task
from app.models.project_budget import ProjectBudget
from app.models.project import Project, ProjectStatus
from app.schemas.project import ProjectResponse


def _calc_progress(db: Session, project_id: int) -> int:
    """タスクの進捗率の平均をSQLで算出する"""
    result = (
        db.query(func.avg(Task.progress)).filter(Task.project_id == project_id).scalar()
    )
    return int(result or 0)


def _calc_schedule_rate(project: Project) -> int:
    """案件期間に対する経過率を算出する"""
    if not project.start_date or not project.end_date:
        return 0

    start = project.start_date.date()
    end = project.end_date.date()
    today = date.today()

    if today <= start:
        return 0
    if today >= end:
        return 100

    total_days = (end - start).days
    elapsed_days = (today - start).days

    if total_days <= 0:
        return 0

    return int(elapsed_days / total_days * 100)


def _judge_alert(progress: int, schedule_rate: int, consumption_rate: int | None):
    """進捗・予算から危険度を判定する"""
    alert_reasons: list[str] = []

    schedule_diff = progress - schedule_rate

    if schedule_diff <= -20:
        alert_reasons.append("schedule_delay_danger")
    elif schedule_diff <= -10:
        alert_reasons.append("schedule_delay_warning")

    if consumption_rate is not None:
        budget_diff = progress - consumption_rate

        if budget_diff <= -25:
            alert_reasons.append("budget_over_danger")
        elif budget_diff <= -15:
            alert_reasons.append("budget_over_warning")

    if any("danger" in reason for reason in alert_reasons):
        return "danger", ",".join(alert_reasons)

    if any("warning" in reason for reason in alert_reasons):
        return "warning", ",".join(alert_reasons)

    return "normal", ""


def to_response(db: Session, project: Project) -> ProjectResponse:
    """ProjectをProjectResponseに変換する（progress・予算情報・アラート情報付き）"""

    data = ProjectResponse.model_validate(project)

    data.department_name = project.department.name if project.department else None

    data.applicant_name = project.applicant.name if project.applicant else None

    progress = _calc_progress(db, project.id)
    data.progress = progress

    consumption_rate = None

    budget = (
        db.query(ProjectBudget).filter(ProjectBudget.project_id == project.id).first()
    )
    if budget:
        data.actual_amount = budget.actual_amount
        if budget.budget_amount > 0:
            consumption_rate = int(budget.actual_amount / budget.budget_amount * 100)
            data.consumption_rate = consumption_rate

    if project.status not in {
        ProjectStatus.APPROVED,
        ProjectStatus.IN_PROGRESS,
    }:
        data.alert_level = "normal"
        data.alert_reason = ""
        return data

    schedule_rate = _calc_schedule_rate(project)
    alert_level, alert_reason = _judge_alert(
        progress=progress,
        schedule_rate=schedule_rate,
        consumption_rate=consumption_rate,
    )

    data.alert_level = alert_level
    data.alert_reason = alert_reason

    return data
