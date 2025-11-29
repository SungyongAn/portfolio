from datetime import datetime
from db_utils import get_db

from app.models.chat_model import ChatRoom
from app.models.renrakucho_model import RenrakuchoEntryModel
from app.models.accounts_model import Account


def seed_sample_data():
    print("Seeding sample data...")
    db = next(get_db())
    
    # Chat Rooms
    chat_rooms = [
        {
            "name": "1年A組 連絡用",
            "description": "1年A組の生徒と教員の連絡チャットルームです",
            "creator_id": 3 # Teacher ID (assuming ID 3 exists from seed_accounts)
        },
        {
            "name": "職員室",
            "description": "教員同士の連絡用チャットルームです",
            "creator_id": 3
        }
    ]
    
    count_rooms = 0
    for data in chat_rooms:
        exists = db.query(ChatRoom).filter(ChatRoom.name == data["name"]).first()
        if not exists:
            room = ChatRoom(**data)
            db.add(room)
            count_rooms += 1
    print(f"Seeded {count_rooms} chat rooms.")

    # Renrakucho Entries
    today = datetime.now().date()
    # Assuming student IDs start from 6 based on seed_accounts order (1 admin, 1 nurse, 3 teachers)
    # But IDs are auto-increment, so we should query to be safe, or just assume for sample data if fresh db.
    # Let's assume fresh DB for simplicity as per original script logic.
    
    entries = [
        {
            "student_id": 6,
            "submitted_date": today,
            "target_date": today,
            "physical_condition": 5,
            "mental_state": 5,
            "physical_mental_notes": "今日も元気です！",
            "daily_reflection": "【授業】数学のテストで満点が取れました。",
            "is_read": False
        },
        {
            "student_id": 7,
            "submitted_date": today,
            "target_date": today,
            "physical_condition": 4,
            "mental_state": 5,
            "physical_mental_notes": "体調良好です",
            "daily_reflection": "【授業】英語のプレゼンテーションをしました。",
            "is_read": False
        },
        {
            "student_id": 8,
            "submitted_date": today,
            "target_date": today,
            "physical_condition": 5,
            "mental_state": 4,
            "physical_mental_notes": "",
            "daily_reflection": "【授業】理科の実験が面白かったです。",
            "is_read": False
        }
    ]
    
    count_entries = 0
    for data in entries:
        # Check if exists (simple check by student_id and date)
        exists = db.query(RenrakuchoEntryModel).filter(
            RenrakuchoEntryModel.student_id == data["student_id"],
            RenrakuchoEntryModel.target_date == data["target_date"]
        ).first()
        
        if not exists:
            entry = RenrakuchoEntryModel(**data)
            db.add(entry)
            count_entries += 1
            
    db.commit()
    print(f"Seeded {count_entries} renrakucho entries.")

if __name__ == "__main__":
    seed_sample_data()
