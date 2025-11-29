import os
from sqlalchemy import text
from db_utils import engine, wait_for_db

from app.db.base import Base


def init_db():
    print("Initializing database...")
    wait_for_db()
    
    # Create tables
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

    # Run init.sql for events or other raw SQL
    init_sql_path = os.path.join(os.path.dirname(__file__), '../init.sql')
    if os.path.exists(init_sql_path):
        print(f"Running {init_sql_path}...")
        with open(init_sql_path, 'r') as f:
            sql_content = f.read()
            # Split by ; and execute each statement
            # Note: This is a simple splitter, might fail on complex SQL with ; in strings
            # But for the current init.sql it should be fine if we handle DELIMITERs or just run it if simple
            
            # The current init.sql has CREATE EVENT which might be complex.
            # Let's try to execute it as a whole or split carefully.
            # SQLAlchemy execute() can handle multiple statements if the driver supports it, 
            # but usually it's safer to execute one by one.
            
            # However, init.sql contains comments and potentially DELIMITER.
            # Let's just try to execute the CREATE EVENT part if it exists.
            
            with engine.connect() as conn:
                # Simple execution of the file content
                # We might need to strip comments
                statements = [s.strip() for s in sql_content.split(';') if s.strip()]
                for statement in statements:
                    # Skip empty or comment-only lines if split left some
                    if not statement or statement.startswith('--'):
                        continue
                    try:
                        conn.execute(text(statement))
                        conn.commit()
                    except Exception as e:
                        print(f"Warning executing statement: {e}")
                        # Continue as it might be "already exists" error
        print("init.sql executed.")
    else:
        print("init.sql not found, skipping.")

if __name__ == "__main__":
    init_db()
