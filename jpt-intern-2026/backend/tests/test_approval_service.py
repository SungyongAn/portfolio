import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.models.project import ProjectStatus
from app.services.project.approval_service import approve_project
from app.schemas.project import ApprovalRequest


class TestApproveProject:
    def _make_approval(self, reject_reason=None):
        approval = MagicMock(spec=ApprovalRequest)
        approval.reject_reason = reject_reason
        return approval

    @patch("app.services.project.approval_service.get_project_or_404")
    @patch("app.services.project.approval_service.notify_applicant")
    @patch("app.services.project.approval_service.push_notification")
    def test_dept_manager_approve(
        self, mock_push, mock_notify, mock_get, db, dept_manager, project
    ):
        """部門管理者が一次承認するとPENDING_HQに遷移する"""
        project.status = ProjectStatus.PENDING_DEPT
        project.department_id = dept_manager.department_id
        mock_get.return_value = project
        db.query.return_value.filter.return_value.all.return_value = []

        with patch("app.services.project.approval_service.to_response"):
            approve_project(db, project.id, self._make_approval(), dept_manager)
            assert project.status == ProjectStatus.PENDING_HQ

    @patch("app.services.project.approval_service.get_project_or_404")
    @patch("app.services.project.approval_service.notify_applicant")
    def test_dept_manager_reject(
        self, mock_notify, mock_get, db, dept_manager, project
    ):
        """部門管理者が却下するとREJECTEDに遷移する"""
        project.status = ProjectStatus.PENDING_DEPT
        project.department_id = dept_manager.department_id
        mock_get.return_value = project

        with patch("app.services.project.approval_service.to_response"):
            approve_project(
                db, project.id, self._make_approval("予算不足"), dept_manager
            )
            assert project.status == ProjectStatus.REJECTED
            assert project.reject_reason == "予算不足"

    @patch("app.services.project.approval_service.get_project_or_404")
    @patch("app.services.project.approval_service.notify_applicant")
    def test_hq_manager_approve(self, mock_notify, mock_get, db, hq_manager, project):
        """本部管理者が最終承認するとAPPROVEDに遷移する"""
        project.status = ProjectStatus.PENDING_HQ
        mock_get.return_value = project

        with patch("app.services.project.approval_service.to_response"):
            approve_project(db, project.id, self._make_approval(), hq_manager)
            assert project.status == ProjectStatus.APPROVED

    @patch("app.services.project.approval_service.get_project_or_404")
    @patch("app.services.project.approval_service.notify_applicant")
    def test_hq_manager_reject(self, mock_notify, mock_get, db, hq_manager, project):
        """本部管理者が却下するとREJECTEDに遷移する"""
        project.status = ProjectStatus.PENDING_HQ
        mock_get.return_value = project

        with patch("app.services.project.approval_service.to_response"):
            approve_project(
                db, project.id, self._make_approval("スコープ過大"), hq_manager
            )
            assert project.status == ProjectStatus.REJECTED

    @patch("app.services.project.approval_service.get_project_or_404")
    def test_wrong_status_raises_error(self, mock_get, db, dept_manager, project):
        """不正なステータスの案件を承認しようとすると400エラー"""
        project.status = ProjectStatus.APPROVED
        project.department_id = dept_manager.department_id
        mock_get.return_value = project

        with pytest.raises(HTTPException) as exc:
            approve_project(db, project.id, self._make_approval(), dept_manager)
        assert exc.value.status_code == 400

    @patch("app.services.project.approval_service.get_project_or_404")
    def test_other_dept_manager_cannot_approve(
        self, mock_get, db, dept_manager, project
    ):
        """他部門の管理者は承認不可"""
        project.status = ProjectStatus.PENDING_DEPT
        project.department_id = 99
        mock_get.return_value = project

        with pytest.raises(HTTPException) as exc:
            approve_project(db, project.id, self._make_approval(), dept_manager)
        assert exc.value.status_code == 403
