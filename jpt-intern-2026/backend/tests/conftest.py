import pytest
from unittest.mock import MagicMock
from app.models.user import User, UserRole
from app.models.project import Project, ProjectStatus


@pytest.fixture
def db():
    """モックDBセッション"""
    return MagicMock()


@pytest.fixture
def applicant():
    user = MagicMock(spec=User)
    user.id = 1
    user.role = UserRole.APPLICANT
    user.department_id = 1
    return user


@pytest.fixture
def dept_manager():
    user = MagicMock(spec=User)
    user.id = 2
    user.role = UserRole.DEPT_MANAGER
    user.department_id = 1
    return user


@pytest.fixture
def hq_manager():
    user = MagicMock(spec=User)
    user.id = 3
    user.role = UserRole.HQ_MANAGER
    user.department_id = 3
    return user


@pytest.fixture
def project():
    p = MagicMock(spec=Project)
    p.id = 1
    p.name = "テスト案件"
    p.applicant_id = 1
    p.department_id = 1
    p.status = ProjectStatus.PENDING_DEPT
    return p
