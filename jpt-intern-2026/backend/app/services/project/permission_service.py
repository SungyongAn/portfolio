from fastapi import HTTPException, status
from app.models.project import Project, ProjectStatus
from app.models.user import User, UserRole


def check_project_access(project: Project, current_user: User) -> None:
    if current_user.role == UserRole.HQ_MANAGER:
        return

    if current_user.role == UserRole.DEPT_MANAGER:
        if project.department_id == current_user.department_id:
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="権限がありません",
        )

    if current_user.role == UserRole.TASK_MEMBER:
        if project.department_id == current_user.department_id:
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="権限がありません",
        )

    if project.applicant_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="権限がありません",
        )


def check_project_editable(project: Project, current_user: User) -> None:
    """案件編集権限チェック
    - 申請者は自身の案件のみ・PENDING_DEPT状態のみ編集可
    """
    if project.applicant_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作を行う権限がありません",
        )
    if project.status != ProjectStatus.PENDING_DEPT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="この案件は編集できません",
        )


def check_approval_permission(project: Project, current_user: User) -> None:
    """承認操作の権限チェック
    - 部門管理者：PENDING_DEPT・自部門のみ承認可
    - 本部管理者：PENDING_HQのみ承認可
    """
    if current_user.role == UserRole.DEPT_MANAGER:
        if project.status != ProjectStatus.PENDING_DEPT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="この案件は一次承認待ちではありません",
            )
        if project.department_id != current_user.department_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="この操作を行う権限がありません",
            )

    elif current_user.role == UserRole.HQ_MANAGER:
        if project.status != ProjectStatus.PENDING_HQ:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="この案件は最終承認待ちではありません",
            )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作を行う権限がありません",
        )


def check_budget_permission(project: Project, current_user: User) -> None:
    """予算・工数・経費の操作権限チェック
    - 申請者は自身の案件のみ操作可
    """
    if (
        current_user.role == UserRole.APPLICANT
        and project.applicant_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="この操作を行う権限がありません",
        )


def check_start_permission(project: Project, current_user: User) -> None:
    """着手操作の権限チェック
    - 申請者・部門管理者・本部管理者が対象案件に対して操作可
    """
    if (
        current_user.role not in [UserRole.DEPT_MANAGER, UserRole.HQ_MANAGER]
        and current_user.id != project.applicant_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="権限がありません",
        )
    if project.status != ProjectStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="承認済み案件のみ着手できます",
        )


def check_complete_permission(project: Project, current_user: User) -> None:
    """完了操作の権限チェック
    - 部門管理者・本部管理者のみ操作可
    """
    if current_user.role not in [UserRole.DEPT_MANAGER, UserRole.HQ_MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="権限がありません",
        )
    if project.status != ProjectStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="進行中案件のみ完了できます",
        )


def check_dept_access(department_id: int, current_user: User) -> None:
    """部門へのアクセス権限チェック
    - 本部管理者：全部門アクセス可
    - 部門管理者：自部門のみ
    - タスクメンバー：自部門のみ
    - 申請者：アクセス不可
    """
    if current_user.role == UserRole.HQ_MANAGER:
        return

    if current_user.role in (UserRole.DEPT_MANAGER, UserRole.TASK_MEMBER):
        if current_user.department_id == department_id:
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="権限がありません",
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="権限がありません",
    )
