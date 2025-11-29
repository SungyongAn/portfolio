from app.models.accounts_model import Account
from app.models.renrakucho_model import RenrakuchoEntryModel
from app.services.auth import get_password_hash
from datetime import date

def test_create_renrakucho(client, db_session):
    # Create student
    hashed_password = get_password_hash("studentpass")
    student = Account(
        name="Student", password=hashed_password, role="student", 
        status="enrolled", grade=1, class_name="A", enrollment_year=2024
    )
    db_session.add(student)
    db_session.commit()
    
    # Login
    login_res = client.post("/auth/login", json={"id": student.id, "name": "Student", "password": "studentpass"})
    token = login_res.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create entry
    payload = {
        "student_id": student.id,
        "submitted_date": str(date.today()),
        "target_date": str(date.today()),
        "physical_condition": 3,
        "mental_state": 3,
        "physical_mental_notes": "Good",
        "daily_reflection": "Studied hard"
    }
    
    response = client.post("/renrakucho-management/entry-renrakucho", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    # Verify in DB
    entry = db_session.query(RenrakuchoEntryModel).filter_by(student_id=student.id).first()
    assert entry is not None
    assert entry.daily_reflection == "Studied hard"
