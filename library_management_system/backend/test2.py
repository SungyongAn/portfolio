from routes.services.material_service import MaterialService
from routes.db import get_db

db = next(get_db())
service = MaterialService(db)
service.print_all_materials()
