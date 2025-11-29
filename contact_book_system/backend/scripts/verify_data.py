import sys
from sqlalchemy import text
from db_utils import get_db, verify_password

from app.models.accounts_model import Account

def verify_data():
    print("\nVerifying setup...")
    db = next(get_db())
    
    # Check account counts
    print("\nAccount counts by role:")
    results = db.execute(text("SELECT role, COUNT(*) FROM accounts GROUP BY role ORDER BY role")).fetchall()
    for role, count in results:
        print(f"  {role:15}: {count}")
        
    # Check character encoding
    print("\nCharacter encoding check:")
    admin = db.query(Account).filter(Account.id == 1).first()
    if admin:
        print(f"  ID 1 Name: {admin.name}")
        if '?' not in admin.name:
            print("  ✓ Encoding OK")
        else:
            print("  ⚠️ Possible encoding issue")
            
    # Check passwords
    print("\nPassword verification:")
    passwords = {
        'admin': 'admin123',
        'school_nurse': 'nurse123',
        'teacher': 'teacher123',
        'student': 'student123'
    }
    
    all_valid = True
    for role, password in passwords.items():
        account = db.query(Account).filter(Account.role == role).first()
        if account:
            is_valid = verify_password(password, account.password)
            status = "✓ OK" if is_valid else "✗ NG"
            print(f"  {role:15}: {status}")
            if not is_valid:
                all_valid = False
        else:
            print(f"  {role:15}: Not found")
            
    if all_valid:
        print("\n✅ Verification successful!")
        return True
    else:
        print("\n⚠️ Verification failed!")
        return False

if __name__ == "__main__":
    if not verify_data():
        sys.exit(1)
