from datetime import date

from sqlalchemy.orm import Session

from app.models.user import User, UserRole
from app.services.dashboard.dashboard_builders import (
    build_department_summaries,
    build_owner_summaries,
    build_project_item,
    build_risk_projects,
    build_status_summary,
)
from app.services.dashboard.dashboard_calc_service import (
    calc_consumption_rate,
    to_status_value,
)
from app.services.dashboard.dashboard_query_service import (
    get_target_projects,
    get_target_tasks,
    get_unread_notification_count,
)
from app.services.dashboard.dashboard_task_service import (
    build_task_items,
    build_task_member_summary,
)

DONE_TASK_STATUSES = {"DONE", "COMPLETED"}


def _to_status_name(status) -> str:
    """Enum / str のどちらでも比較できるように文字列化する"""
    return getattr(status, "value", status)


def _build_overdue_task_count_by_department(projects, tasks) -> dict[str, int]:
    """
    部門別の期限超過タスク件数を集計する。

    - due_date が今日より前
    - 完了済みステータスではない
    - 対象ユーザーが参照可能な projects / tasks の範囲内で集計
    """
    today = date.today()

    project_department_map = {
        project.id: project.department.name
        for project in projects
        if project.department is not None
    }

    overdue_counts: dict[str, int] = {
        department_name: 0 for department_name in project_department_map.values()
    }

    for task in tasks:
        if not task.due_date:
            continue

        if task.due_date >= today:
            continue

        task_status = _to_status_name(task.status)
        if task_status in DONE_TASK_STATUSES:
            continue

        department_name = project_department_map.get(task.project_id)
        if not department_name:
            continue

        overdue_counts[department_name] = overdue_counts.get(department_name, 0) + 1

    return overdue_counts


def _merge_overdue_task_count_to_departments(
    department_summaries: list[dict],
    overdue_counts: dict[str, int],
) -> list[dict]:
    """部門別サマリーへ期限超過タスク件数を追加する"""
    return [
        {
            **department,
            "overdue_task_count": overdue_counts.get(
                department["department_name"],
                0,
            ),
        }
        for department in department_summaries
    ]


def get_alert_dashboard(db: Session, current_user: User):
    """
    既存API互換用：/api/dashboard/alerts

    管理者向けモニタリング方針に合わせ、
    危険・注意案件一覧を返す。
    """
    projects = get_target_projects(db, current_user)
    project_items = [build_project_item(project) for project in projects]

    return build_risk_projects(project_items)


def get_dashboard_summary(db: Session, current_user: User):
    """
    管理者向け案件モニタリングPoC版ダッシュボードAPI

    - HQ_MANAGER: 全社・部門横断の案件/予算/危険案件を可視化
    - DEPT_MANAGER: 自部門の案件/予算/危険案件を可視化
    - APPLICANT: 自分の申請案件状況を可視化
    - TASK_MEMBER: 自担当タスク状況を可視化
    """
    projects = get_target_projects(db, current_user)
    tasks = get_target_tasks(db, current_user)

    project_items = [build_project_item(project) for project in projects]

    total_projects = len(project_items)
    total_budget = sum(item["budget_amount"] for item in project_items)
    total_actual = sum(item["actual_amount"] for item in project_items)

    risk_projects = build_risk_projects(project_items)
    danger_projects = sum(
        1 for item in risk_projects if item["alert_level"] == "danger"
    )
    warning_projects = sum(
        1 for item in risk_projects if item["alert_level"] == "warning"
    )

    status_summary = build_status_summary(project_items)

    overdue_counts_by_department = _build_overdue_task_count_by_department(
        projects,
        tasks,
    )

    department_summaries = _merge_overdue_task_count_to_departments(
        build_department_summaries(project_items),
        overdue_counts_by_department,
    )

    owner_summaries = build_owner_summaries(project_items)

    unread_notifications = get_unread_notification_count(db, current_user)

    active_projects = sum(
        1 for item in project_items if item["status"] in {"APPROVED", "IN_PROGRESS"}
    )

    completed_projects = sum(
        1 for item in project_items if item["status"] == "COMPLETED"
    )

    pending_approvals = sum(
        1 for item in project_items if item["status"] in {"PENDING_DEPT", "PENDING_HQ"}
    )

    budget_warning_count = sum(
        1
        for item in project_items
        if item["status"] in {"APPROVED", "IN_PROGRESS"}
        and item["consumption_rate"] >= 80
    )

    response = {
        "role": to_status_value(current_user.role),
        "summary": {
            # 既存フロント互換
            "unreadNotifications": unread_notifications,
            "pendingApprovals": pending_approvals,
            "inProgressProjects": active_projects,
            "completedProjects": completed_projects,
            "dangerProjects": danger_projects,
            "warningProjects": warning_projects,
            "budgetWarningCount": budget_warning_count,
            # 新ダッシュボード用
            "totalProjects": total_projects,
            "totalBudget": total_budget,
            "totalActual": total_actual,
            "totalConsumptionRate": calc_consumption_rate(
                total_budget,
                total_actual,
            ),
            "activeProjects": active_projects,
            "completedProjectCount": completed_projects,
            "pendingApprovalCount": pending_approvals,
            "riskProjectCount": len(risk_projects),
        },
        "statusSummary": status_summary,
        "departments": department_summaries,
        "owners": owner_summaries,
        "riskProjects": risk_projects,
        "projects": project_items,
    }

    if current_user.role == UserRole.TASK_MEMBER:
        response["taskSummary"] = build_task_member_summary(tasks)
        response["tasks"] = build_task_items(tasks)

    if current_user.role == UserRole.APPLICANT:
        response["applicantSummary"] = {
            "draft": status_summary["draft"],
            "pending": status_summary["pending_dept"] + status_summary["pending_hq"],
            "approved": status_summary["approved"],
            "inProgress": status_summary["in_progress"],
            "completed": status_summary["completed"],
            "rejected": status_summary["rejected"],
        }

    return response
