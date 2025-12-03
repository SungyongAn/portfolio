from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from routes.models.accounts_model import Account, RoleEnum, StatusEnum
from routes.schemas.accounts_schema import (
    AccountRegisterRequest,
    AccountSearchPayload,
    AccountUpdatePayload
)
from routes.repositories.account_repository import (
    AccountRepository,
    TeacherRoleRepository,
    SubjectRepository
)

# パスワードハッシュ化の設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AccountService:

    # アカウント登録
    @staticmethod
    def register_account(db: Session, register_data: AccountRegisterRequest):
        try:
            # roleをEnumに変換
            try:
                role_enum = RoleEnum(register_data.role.lower())
            except ValueError:
                return {"success": False, "message": f"Invalid role: {register_data.role}"}

            grade = register_data.grade
            current_year = datetime.now().year

            enrollment_year = register_data.enrollment_year or (
                current_year - (grade - 1) if role_enum == RoleEnum.student else current_year
            )

            graduation_year = register_data.graduation_year or (
                enrollment_year + 3 if role_enum == RoleEnum.student else 2099
            )

            # 重複チェック（リポジトリを使用）
            existing_account = AccountRepository.find_by_name_grade_class(
                db,
                register_data.name,
                grade,
                register_data.class_name
            )
            
            if existing_account:
                return {
                    "success": False,
                    "message": f"Account already exists in {grade}年{register_data.class_name}組"
                }

            teacher_role_id = None
            subject_id = None
            
            # 教員区分の取得（リポジトリを使用）
            if register_data.teacher_role:
                teacher_role = TeacherRoleRepository.find_by_code(db, register_data.teacher_role)
                if teacher_role:
                    teacher_role_id = teacher_role.id
                else:
                    return {
                        "success": False,
                        "message": f"Invalid teacher_role code: {register_data.teacher_role}"
                    }
            
            # 科目の取得（リポジトリを使用）
            if register_data.subject:
                subject = SubjectRepository.find_by_code(db, register_data.subject)
                if subject:
                    subject_id = subject.id
                else:
                    return {
                        "success": False,
                        "message": f"Invalid subject code: {register_data.subject}"
                    }

            # パスワードをハッシュ化
            hashed_password = pwd_context.hash(register_data.password)

            # 新規アカウントの作成（リポジトリを使用）
            new_account = Account(
                grade=grade,
                class_name=register_data.class_name,
                name=register_data.name,
                password=hashed_password,
                enrollment_year=enrollment_year,
                graduation_year=graduation_year,
                status=StatusEnum.enrolled,
                role=role_enum,
                teacher_role_id=teacher_role_id,
                subject_id=subject_id 
            )

            new_account = AccountRepository.create(db, new_account)

            # レスポンス用にコードを取得
            teacher_role_code = None
            subject_code = None
            
            if new_account.teacher_role_id:
                teacher_role = TeacherRoleRepository.find_by_id(db, new_account.teacher_role_id)
                if teacher_role:
                    teacher_role_code = teacher_role.code
            
            if new_account.subject_id:
                subject = SubjectRepository.find_by_id(db, new_account.subject_id)
                if subject:
                    subject_code = subject.code

            return {
                "success": True,
                "message": "Account created successfully",
                "data": {
                    "id": new_account.id,
                    "name": new_account.name,
                    "role": new_account.role.value,
                    "grade": new_account.grade,
                    "class_name": new_account.class_name,
                    "enrollment_year": new_account.enrollment_year,
                    "graduation_year": new_account.graduation_year,
                    "status": new_account.status.value,
                    "teacher_role": teacher_role_code,
                    "subject": subject_code
                }
            }

        except IntegrityError:
            db.rollback()
            return {"success": False, "message": "Account creation failed (duplicate data)"}

        except Exception:
            db.rollback()
            return {"success": False, "message": "Unexpected error"}

    # アカウント検索
    @staticmethod 
    def search_accounts(db: Session, payload: AccountSearchPayload) -> list[dict]:
        # teacher_roleとsubjectをIDに変換
        teacher_role_id = None
        subject_id = None
        
        if payload.teacher_role:
            teacher_role = TeacherRoleRepository.find_by_code(db, payload.teacher_role)
            if teacher_role:
                teacher_role_id = teacher_role.id
        
        if payload.subject:
            subject = SubjectRepository.find_by_code(db, payload.subject)
            if subject:
                subject_id = subject.id
        
        # statusの変換
        status_value = None
        if payload.status:
            status_map = {
                '在校': 'enrolled',
                '卒業': 'graduated',
                '転校': 'transferred',
                '休学': 'on_leave',
                'その他': 'other'
            }
            status_value = status_map.get(payload.status, payload.status)
        
        # リポジトリを使用して検索
        accounts = AccountRepository.search_with_filters(
            db,
            role=payload.role,
            full_name=payload.fullName,
            grade=payload.grade,
            class_name=payload.class_name,
            enrollment_year=payload.enrollment_year,
            status=status_value,
            teacher_role_id=teacher_role_id,
            subject_id=subject_id
        )

        # 管理者権限のアカウント情報を除外
        accounts = accounts.filter(Account.role != RoleEnum.admin)

        # レスポンス形式を整形
        results = []
        for acc in accounts:
            teacher_role_code = None
            subject_code = None
        
            if acc.teacher_role_id:
                teacher_role = TeacherRoleRepository.find_by_id(db, acc.teacher_role_id)
                if teacher_role:
                    teacher_role_code = teacher_role.code
        
            if acc.subject_id:
                subject = SubjectRepository.find_by_id(db, acc.subject_id)
                if subject:
                    subject_code = subject.code
        
            results.append({
                "id": acc.id,
                "role": acc.role.value,
                "fullName": acc.name,
                "grade": acc.grade,
                "className": acc.class_name,
                "enrollmentYear": acc.enrollment_year,
                "graduationYear": acc.graduation_year,
                "status": acc.status.value,
                "teacher_role": teacher_role_code,
                "subject": subject_code
            })
    
        return results

    # アカウント更新
    @staticmethod
    def update_accounts(db: Session, updates: list[AccountUpdatePayload]):
        role_map = {
            'student': RoleEnum.student,
            'teacher': RoleEnum.teacher,
            'admin': RoleEnum.admin,
            'school_nurse': RoleEnum.school_nurse
        }
        status_map = {
            'enrolled': StatusEnum.enrolled,
            'graduated': StatusEnum.graduated,
            'transferred': StatusEnum.transferred,
            'suspended': StatusEnum.on_leave,
            'on_leave': StatusEnum.on_leave,
            'other': StatusEnum.other
        }

        updated_count = 0
        errors = []

        try:
            for item in updates:
                # リポジトリを使用してアカウント取得
                account = AccountRepository.find_by_id(db, item.id)
                if not account:
                    errors.append(f"ID {item.id} のアカウントが見つかりません")
                    continue

                role_enum = role_map.get(item.role.lower())
                if not role_enum:
                    errors.append(f"ID {item.id}: 無効な役割 '{item.role}'")
                    continue

                status_enum = status_map.get(item.status.lower())
                if not status_enum:
                    errors.append(f"ID {item.id}: 無効な状態 '{item.status}'")
                    continue

                # 基本情報の更新
                account.role = role_enum
                account.name = item.fullName
                account.grade = item.grade
                account.class_name = item.className
                account.status = status_enum

                # 教師フィールドの更新（リポジトリを使用）
                if hasattr(item, 'teacher_role') and item.teacher_role:
                    teacher_role = TeacherRoleRepository.find_by_code(db, item.teacher_role)
                    if teacher_role:
                        account.teacher_role_id = teacher_role.id
                    else:
                        errors.append(f"ID {item.id}: 無効な教員区分 '{item.teacher_role}'")
                        continue
                
                if hasattr(item, 'subject') and item.subject:
                    subject = SubjectRepository.find_by_code(db, item.subject)
                    if subject:
                        account.subject_id = subject.id
                    else:
                        errors.append(f"ID {item.id}: 無効な教科 '{item.subject}'")
                        continue

                # パスワードが提供されている場合はハッシュ化して更新
                if hasattr(item, 'password') and item.password:
                    account.password = pwd_context.hash(item.password)

                updated_count += 1

            if updated_count > 0:
                db.commit()

            return {
                "success": len(errors) == 0,
                "message": f"{updated_count}件更新しました。" + (" エラーあり。" if errors else ""),
                "data": {
                    "updated_count": updated_count,
                    "errors": errors
                }
            }

        except Exception:
            db.rollback()
            return {"success": False, "message": "更新中にエラーが発生しました"}

    """ 以下、未使用 """
    # ログイン認証
    @staticmethod
    def verify_login(db: Session, name: str, password: str):
        # リポジトリを使用してアカウント検索
        account = AccountRepository.find_by_name(db, name)
        
        if not account:
            return {"success": False, "message": "Account not found"}
        
        # ハッシュ化されたパスワードと比較
        if not pwd_context.verify(password, account.password):
            return {"success": False, "message": "Invalid password"}
        
        return {
            "success": True,
            "message": "Login successful",
            "data": {
                "id": account.id,
                "name": account.name,
                "role": account.role.value,
                "grade": account.grade,
                "class_name": account.class_name,
                "status": account.status.value
            }
        }

    # パスワードリセット（管理者用）
    @staticmethod
    def reset_password(db: Session, account_id: int, new_password: str):
        try:
            # リポジトリを使用してアカウント取得
            account = AccountRepository.find_by_id(db, account_id)
            
            if not account:
                return {"success": False, "message": "Account not found"}
            
            # 新しいパスワードをハッシュ化
            account.password = pwd_context.hash(new_password)
            AccountRepository.update(db, account)
            
            return {
                "success": True,
                "message": "Password reset successfully"
            }
            
        except Exception:
            db.rollback()
            return {"success": False, "message": "Password reset failed"}
