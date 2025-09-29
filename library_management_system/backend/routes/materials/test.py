from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from routes.models import materials  # モデルをインポート

# MySQL 接続情報
engine = create_engine("mysql+pymysql://appuser:apppass@localhost:3306/library_system")
SessionLocal = sessionmaker(bind=engine)


def get_material_by_barcode(barcode: str):
    session = SessionLocal()
    try:
        existing_material = session.query(materials.Material).filter(
            materials.Material.barcode == barcode
        ).first()

        if existing_material:
            print(
                f"ID: {existing_material.material_id}, "
                f"バーコード: {existing_material.barcode}, "
                f"タイトル: {getattr(existing_material, 'title', None)}, "
                f"著者: {getattr(existing_material, 'author', None)}"
            )
        else:
            print("該当する資料はありません。")

    finally:
        session.close()
