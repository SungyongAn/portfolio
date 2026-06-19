from datetime import date

from app.models.task import Task, TaskStatus
from app.services.dashboard.dashboard_calc_service import to_status_value


def build_task_member_summary(tasks: list[Task]) -> dict:
    """担当者向けタスク集計"""

    active_tasks = [task for task in tasks if task.status != TaskStatus.DONE]

    summary = {
        "total_tasks": len(active_tasks),
        "todo": 0,
        "in_progress": 0,
        "in_review": 0,
        "done": 0,
        "overdue": 0,
        "today_deadline": 0,
    }

    today = date.today()

    for task in tasks:
        if task.status == TaskStatus.TODO:
            summary["todo"] += 1
        elif task.status == TaskStatus.IN_PROGRESS:
            summary["in_progress"] += 1
        elif task.status == TaskStatus.IN_REVIEW:
            summary["in_review"] += 1
        elif task.status == TaskStatus.DONE:
            summary["done"] += 1

        if task.due_date and task.status != TaskStatus.DONE:
            if task.due_date < today:
                summary["overdue"] += 1
            elif task.due_date == today:
                summary["today_deadline"] += 1

    return summary


def build_task_items(tasks: list[Task]) -> list[dict]:
    """担当者向けタスク一覧"""
    today = date.today()

    task_items = []

    for task in tasks:
        if task.status == TaskStatus.DONE:
            continue

        priority = "normal"

        if task.due_date and task.due_date < today:
            priority = "danger"
        elif task.due_date and task.due_date == today:
            priority = "warning"

        task_items.append(
            {
                "id": task.id,
                "name": task.name,
                "status": to_status_value(task.status),
                "progress": task.progress,
                "project_id": task.project_id,
                "project_name": task.project.name if task.project else None,
                "department_name": (
                    task.project.department.name
                    if task.project and task.project.department
                    else None
                ),
                "assignee_name": task.assignee.name if task.assignee else None,
                "start_date": task.start_date.isoformat() if task.start_date else None,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": priority,
            }
        )

    return sorted(
        task_items,
        key=lambda x: (
            x["priority"] != "danger",
            x["priority"] != "warning",
            x["due_date"] or "9999-12-31",
        ),
    )
