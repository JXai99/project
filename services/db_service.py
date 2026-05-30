import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

"""FOR DATABASE POSTGRESQL"""
# Get DATABASE_URL from environment, fallback to local SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///scores.db")

# Ensure SQLAlchemy-compatible format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Try to create database engine
try:
    engine = create_engine(DATABASE_URL)
except SQLAlchemyError as e:
    print("❌ Database connection failed:", e)
    raise RuntimeError("Failed to connect to the database.") from e


# Query helper
def query_db(query, params=None):
    """Execute a SQL query with optional parameters and return all results."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            return result.mappings().all()
            #return result.fetchall()
    except SQLAlchemyError as e:
        print("❌ Query execution failed:", e)
        return None
    
def write_db(query, params=None):
    """Execute a write (INSERT, UPDATE, DELETE) query and return rowcount."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            conn.commit()  # Explicit commit when using raw connections
            return result.rowcount
    except SQLAlchemyError as e:
        print("❌ Write operation failed:", e)
        return 0
    
   