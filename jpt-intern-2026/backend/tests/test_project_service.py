from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from app.schemas.project import ProjectResponse
from app.services.project.project_service import get_projects


@patch("app.services.project.project_service.apply_project_filters")
@patch("app.services.project.project_service.to_response")
def test_returns_paginated_result(
    mock_response,
    mock_filter,
    db,
    applicant,
):
    """ページネーションが正しく動作する"""

    mock_query = MagicMock()

    # DBから取得されるProjectモック
    mock_projects = [MagicMock() for _ in range(25)]

    mock_query.order_by.return_value.all.return_value = mock_projects
    mock_filter.return_value = mock_query

    now = datetime.now(timezone.utc)

    # ProjectResponseモックを返す
    mock_response.side_effect = [
        ProjectResponse(
            id=i,
            name=f"Project {i}",
            description="test",
            status="APPROVED",
            development_method="WATERFALL",
            applicant_id=1,
            department_id=1,
            budget_amount=100000,
            planned_months=1,
            reject_reason=None,
            alert_level=None,
            alert_reason=None,
            created_at=now,
            updated_at=now,
        )
        for i in range(25)
    ]

    result = get_projects(
        db,
        applicant,
        page=1,
        limit=10,
    )

    assert result.total == 25
    assert len(result.items) == 10
    assert result.page == 1
    assert result.limit == 10
