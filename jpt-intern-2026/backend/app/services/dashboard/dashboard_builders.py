from datetime import date

from app.models.project import Project
from app.models.task import TaskStatus
from app.services.dashboard.dashboard_calc_service import (
    calc_consumption_rate,
    calc_project_progress,
    calc_schedule_rate,
    judge_alert,
    to_status_value,
    calc_cpi,
    calc_spi,
)


def build_project_item(project: Project) -> dict:
    """案件一覧表示用データを構築"""
    tasks = project.tasks or []
    budget = project.budget

    budget_amount = budget.budget_amount if budget else project.budget_amount
    actual_amount = budget.actual_amount if budget else 0
    consumption_rate = calc_consumption_rate(budget_amount, actual_amount)

    progress = calc_project_progress(tasks)
    schedule_rate = calc_schedule_rate(project)

    spi = calc_spi(progress, schedule_rate)
    cpi = calc_cpi(progress, consumption_rate)

    overdue_task_count = sum(
        1
        for task in tasks
        if task.due_date
        and task.due_date < date.today()
        and task.status != TaskStatus.DONE
    )

    alert = judge_alert(
        progress=progress,
        schedule_rate=schedule_rate,
        consumption_rate=consumption_rate,
        overdue_task_count=overdue_task_count,
    )

    return {
        "id": project.id,
        "name": project.name,
        "status": to_status_value(project.status),
        "department_id": project.department_id,
        "department_name": project.department.name if project.department else None,
        "owner_id": project.applicant_id,
        "owner_name": project.applicant.name if project.applicant else None,
        "budget_amount": budget_amount or 0,
        "actual_amount": actual_amount or 0,
        "consumption_rate": consumption_rate,
        "progress": progress,
        "schedule_rate": schedule_rate,
        "overdue_task_count": overdue_task_count,
        "alert_level": alert["level"],
        "alert_reason": alert["reason"],
        "spi": spi,
        "cpi": cpi,
    }


def build_department_summaries(project_items: list[dict]) -> list[dict]:
    """部門別集計"""
    grouped: dict[int, dict] = {}

    for item in project_items:
        department_id = item["department_id"]
        department_name = item["department_name"] or "未設定"

        if department_id not in grouped:
            grouped[department_id] = {
                "department_id": department_id,
                "department_name": department_name,
                "project_count": 0,
                "active_project_count": 0,
                "completed_project_count": 0,
                "budget_amount": 0,
                "actual_amount": 0,
                "consumption_rate": 0,
                "danger_projects": 0,
                "warning_projects": 0,
            }

        row = grouped[department_id]
        row["project_count"] += 1
        row["budget_amount"] += item["budget_amount"]
        row["actual_amount"] += item["actual_amount"]

        if item["status"] in {"APPROVED", "IN_PROGRESS"}:
            row["active_project_count"] += 1

        if item["status"] == "COMPLETED":
            row["completed_project_count"] += 1

        if item["alert_level"] == "danger":
            row["danger_projects"] += 1

        if item["alert_level"] == "warning":
            row["warning_projects"] += 1

    for row in grouped.values():
        row["consumption_rate"] = calc_consumption_rate(
            row["budget_amount"],
            row["actual_amount"],
        )

    return sorted(
        grouped.values(),
        key=lambda x: (x["danger_projects"], x["consumption_rate"]),
        reverse=True,
    )


def build_owner_summaries(project_items: list[dict]) -> list[dict]:
    """管理責任者別集計"""
    grouped: dict[int, dict] = {}

    for item in project_items:
        owner_id = item["owner_id"]
        owner_name = item["owner_name"] or "未設定"

        if owner_id not in grouped:
            grouped[owner_id] = {
                "owner_id": owner_id,
                "owner_name": owner_name,
                "project_count": 0,
                "active_project_count": 0,
                "danger_projects": 0,
                "warning_projects": 0,
                "budget_amount": 0,
                "actual_amount": 0,
                "consumption_rate": 0,
            }

        row = grouped[owner_id]
        row["project_count"] += 1
        row["budget_amount"] += item["budget_amount"]
        row["actual_amount"] += item["actual_amount"]

        if item["status"] in {"APPROVED", "IN_PROGRESS"}:
            row["active_project_count"] += 1

        if item["alert_level"] == "danger":
            row["danger_projects"] += 1

        if item["alert_level"] == "warning":
            row["warning_projects"] += 1

    for row in grouped.values():
        row["consumption_rate"] = calc_consumption_rate(
            row["budget_amount"],
            row["actual_amount"],
        )

    return sorted(
        grouped.values(),
        key=lambda x: (x["danger_projects"], x["consumption_rate"]),
        reverse=True,
    )


def build_status_summary(project_items: list[dict]) -> dict:
    """ステータス別案件数"""
    summary = {
        "draft": 0,
        "pending_dept": 0,
        "pending_hq": 0,
        "approved": 0,
        "in_progress": 0,
        "completed": 0,
        "rejected": 0,
    }

    status_map = {
        "DRAFT": "draft",
        "PENDING_DEPT": "pending_dept",
        "PENDING_HQ": "pending_hq",
        "APPROVED": "approved",
        "IN_PROGRESS": "in_progress",
        "COMPLETED": "completed",
        "REJECTED": "rejected",
    }

    for item in project_items:
        key = status_map.get(item["status"])
        if key:
            summary[key] += 1

    return summary


def build_risk_projects(project_items: list[dict]) -> list[dict]:
    """危険・注意案件一覧"""
    risk_projects = [
        item
        for item in project_items
        if item["alert_level"] in {"danger", "warning"}
        and item["status"] in {"APPROVED", "IN_PROGRESS"}
    ]

    return sorted(
        risk_projects,
        key=lambda x: (
            x["alert_level"] != "danger",
            -x["consumption_rate"],
            -x["overdue_task_count"],
        ),
    )
