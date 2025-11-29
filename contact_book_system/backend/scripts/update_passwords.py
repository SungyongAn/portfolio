import sys
import os
from db_utils import get_db, get_password_hash, verify_password

# Add backend to path to allow imports from app
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.models.accounts_model import Account

def update_passwords():
    print("Updating passwords...")
    db = next(get_db())
    
    # Passwords mapping: role -> plain password
    # Note: The original script mapped password -> role, but role -> password seems more logical for updates
    # However, the original script supported multiple passwords for different roles.
    # Let's stick to the standard passwords defined in other scripts for consistency.
    passwords = {
        'admin': 'admin123',
        'school_nurse': 'nurse123',
        'teacher': 'teacher123',
        'student': 'student123'
    }
    
    total_updated = 0
    
    for role, password in passwords.items():
        hashed = get_password_hash(password)
        
        # Update all accounts with this role
        accounts = db.query(Account).filter(Account.role == role).all()
        for account in accounts:
            account.password = hashed
            total_updated += 1
            print(f"Updated password for {account.name} ({role})")
            
    db.commit()
    print(f"Updated {total_updated} accounts.")
    return True

def verify_passwords():
    print("\nVerifying passwords...")
    db = next(get_db())
    
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
            
    return all_valid

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Update all account passwords to default values.')
    parser.add_argument('--yes', '-y', action='store_true', help='Skip confirmation prompt')
    args = parser.parse_args()

    print("=" * 80)
    print("Contact Book System - Password Update Tool")
    print("=" * 80)
    
    if not args.yes:
        response = input("Update all passwords to defaults? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            sys.exit(0)
        
    if update_passwords():
        if verify_passwords():
            print("\n✅ Password update and verification successful!")
        else:
            print("\n⚠️ Verification failed!")
            sys.exit(1)
    else:
        print("\n❌ Update failed!")
        sys.exit(1)
