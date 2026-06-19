import pytest
from fastapi import HTTPException
from app.models.project import ProjectStatus
from app.services.project.permission_service import (
    check_project_access,
    check_approval_permission,
    check_start_permission,
    check_complete_permission,
)


class TestCheckProjectAccess:
    def test_hq_manager_can_access_any_project(self, hq_manager, project):
        """本部管理者は全案件にアクセス可能"""
        check_project_access(project, hq_manager)  # 例外が出なければOK

    def test_dept_manager_can_access_own_department(self, dept_manager, project):
        """部門管理者は自部門の案件にアクセス可能"""
        project.department_id = dept_manager.department_id
        check_project_access(project, dept_manager)

    def test_dept_manager_cannot_access_other_department(self, dept_manager, project):
        """部門管理者は他部門の案件にアクセス不可"""
        project.department_id = 99
        with pytest.raises(HTTPException) as exc:
            check_project_access(project, dept_manager)
        assert exc.value.status_code == 403

    def test_applicant_can_access_own_project(self, applicant, project):
        """申請者は自身の案件にアクセス可能"""
        project.applicant_id = applicant.id
        check_project_access(project, applicant)

    def test_applicant_cannot_access_others_project(self, applicant, project):
        """申請者は他人の案件にアクセス不可"""
        project.applicant_id = 99
        with pytest.raises(HTTPException) as exc:
            check_project_access(project, applicant)
        assert exc.value.status_code == 403


class TestCheckApprovalPermission:
    def test_dept_manager_can_approve_pending_dept(self, dept_manager, project):
        """部門管理者はPENDING_DEPT案件を承認可能"""
        project.status = ProjectStatus.PENDING_DEPT
        project.department_id = dept_manager.department_id
        check_approval_permission(project, dept_manager)

    def test_dept_manager_cannot_approve_pending_hq(self, dept_manager, project):
        """部門管理者はPENDING_HQ案件を承認不可"""
        project.status = ProjectStatus.PENDING_HQ
        with pytest.raises(HTTPException) as exc:
            check_approval_permission(project, dept_manager)
        assert exc.value.status_code == 400

    def test_hq_manager_can_approve_pending_hq(self, hq_manager, project):
        """本部管理者はPENDING_HQ案件を承認可能"""
        project.status = ProjectStatus.PENDING_HQ
        check_approval_permission(project, hq_manager)

    def test_hq_manager_cannot_approve_pending_dept(self, hq_manager, project):
        """本部管理者はPENDING_DEPT案件を承認不可"""
        project.status = ProjectStatus.PENDING_DEPT
        with pytest.raises(HTTPException) as exc:
            check_approval_permission(project, hq_manager)
        assert exc.value.status_code == 400

    def test_applicant_cannot_approve(self, applicant, project):
        """申請者は承認操作不可"""
        with pytest.raises(HTTPException) as exc:
            check_approval_permission(project, applicant)
        assert exc.value.status_code == 403


class TestCheckStartPermission:
    def test_applicant_can_start_own_project(self, applicant, project):
        """申請者は自身のAPPROVED案件を着手可能"""
        project.status = ProjectStatus.APPROVED
        project.applicant_id = applicant.id
        check_start_permission(project, applicant)

    def test_cannot_start_non_approved_project(self, applicant, project):
        """APPROVED以外の案件は着手不可"""
        project.status = ProjectStatus.PENDING_DEPT
        project.applicant_id = applicant.id
        with pytest.raises(HTTPException) as exc:
            check_start_permission(project, applicant)
        assert exc.value.status_code == 400


class TestCheckCompletePermission:
    def test_dept_manager_can_complete_in_progress(self, dept_manager, project):
        """部門管理者はIN_PROGRESS案件を完了可能"""
        project.status = ProjectStatus.IN_PROGRESS
        check_complete_permission(project, dept_manager)

    def test_applicant_cannot_complete(self, applicant, project):
        """申請者は完了操作不可"""
        project.status = ProjectStatus.IN_PROGRESS
        with pytest.raises(HTTPException) as exc:
            check_complete_permission(project, applicant)
        assert exc.value.status_code == 403

    def test_cannot_complete_non_in_progress(self, dept_manager, project):
        """IN_PROGRESS以外の案件は完了不可"""
        project.status = ProjectStatus.APPROVED
        with pytest.raises(HTTPException) as exc:
            check_complete_permission(project, dept_manager)
        assert exc.value.status_code == 400
