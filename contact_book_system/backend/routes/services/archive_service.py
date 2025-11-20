from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Any


class ArchiveService:
    """アーカイブ管理サービス"""
    
    @staticmethod
    def get_statistics(db: Session) -> list[dict[str, Any]]:
        """
        アーカイブ統計を取得
        """
        try:
            result = db.execute(text("CALL get_archive_statistics()"))
            rows = result.fetchall()
            
            statistics = []
            for row in rows:
                statistics.append({
                    "data_type": row[0],
                    "record_count": row[1],
                    "oldest_date": row[2],
                    "newest_date": row[3],
                    "size_mb": float(row[4]) if row[4] else 0.0
                })
            
            return {
                "success": True,
                "data": statistics
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to get statistics: {str(e)}"
            }
    
    @staticmethod
    def execute_archive(db: Session, archive_years: int = 3) -> dict[str, Any]:
        """
        アーカイブを実行
        """
        try:
            # ストアドプロシージャを実行
            result = db.execute(
                text("CALL archive_old_renrakucho(:years)"),
                {"years": archive_years}
            )
            row = result.fetchone()
            db.commit()
            
            return {
                "success": bool(row[0]),
                "message": row[1],
                "data": {
                    "records_archived": row[2],
                    "cutoff_date": row[3]
                }
            }
            
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "message": f"Archive execution failed: {str(e)}"
            }
    
    @staticmethod
    def execute_deletion(db: Session, retention_years: int = 5) -> dict[str, Any]:
        """
        期限切れデータを削除
        """
        try:
            # ストアドプロシージャを実行
            result = db.execute(
                text("CALL delete_expired_renrakucho(:years)"),
                {"years": retention_years}
            )
            row = result.fetchone()
            db.commit()
            
            return {
                "success": bool(row[0]),
                "message": row[1],
                "data": {
                    "records_deleted": row[2],
                    "cutoff_date": row[3],
                    "backup_file": row[4] if len(row) > 4 else None
                }
            }
            
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "message": f"Deletion execution failed: {str(e)}"
            }
    
    @staticmethod
    def get_deletion_logs(
        db: Session, 
        limit: int = 50
    ) -> list[dict[str, Any]]:
        """
        削除ログを取得
        """
        try:
            query = text("""
                SELECT 
                    id, deletion_date, table_name, records_deleted,
                    date_range_from, date_range_to, reason, 
                    executed_by, backup_file
                FROM data_deletion_log
                ORDER BY deletion_date DESC
                LIMIT :limit
            """)
            
            result = db.execute(query, {"limit": limit})
            rows = result.fetchall()
            
            logs = []
            for row in rows:
                logs.append({
                    "id": row[0],
                    "deletion_date": row[1],
                    "table_name": row[2],
                    "records_deleted": row[3],
                    "date_range_from": row[4],
                    "date_range_to": row[5],
                    "reason": row[6],
                    "executed_by": row[7],
                    "backup_file": row[8]
                })
            
            return {
                "success": True,
                "data": logs
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to get deletion logs: {str(e)}"
            }
    
    @staticmethod
    def search_archive(
        db: Session,
        student_name: str = None,
        year: int = None,
        month: int = None,
        limit: int = 100
    ) -> list[dict[str, Any]]:
        """
        アーカイブデータを検索
        """
        try:
            # ベースクエリ
            query_str = """
                SELECT 
                    a.name as student_name,
                    a.grade,
                    a.class_name,
                    r.target_date,
                    r.submitted_date,
                    r.physical_condition,
                    r.mental_state,
                    r.daily_reflection,
                    r.is_read
                FROM renrakucho_entries_archive r
                JOIN accounts a ON r.student_id = a.id
                WHERE 1=1
            """
            
            params = {}
            
            # 検索条件を追加
            if student_name:
                query_str += " AND a.name LIKE :student_name"
                params["student_name"] = f"%{student_name}%"
            
            if year:
                query_str += " AND YEAR(r.target_date) = :year"
                params["year"] = year
            
            if month:
                query_str += " AND MONTH(r.target_date) = :month"
                params["month"] = month
            
            query_str += " ORDER BY r.target_date DESC LIMIT :limit"
            params["limit"] = limit
            
            result = db.execute(text(query_str), params)
            rows = result.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    "student_name": row[0],
                    "grade": row[1],
                    "class_name": row[2],
                    "target_date": row[3],
                    "submitted_date": row[4],
                    "physical_condition": row[5],
                    "mental_state": row[6],
                    "daily_reflection": row[7],
                    "is_read": row[8]
                })
            
            return {
                "success": True,
                "data": results
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Archive search failed: {str(e)}"
            }
