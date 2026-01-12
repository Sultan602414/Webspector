"""Database migration script to add Action and LLMAnalysis tables.

Run this after upgrading the codebase to add new tables for action-level tracking.
"""

from dashboard.db import init_engine, Base, get_engine

def migrate():
    """Create new tables if they don't exist."""
    print("Running database migration...")
    
    # Initialize engine from existing database
    import os
    from pathlib import Path
    
    project_root = Path(__file__).parent
    db_url = os.getenv("DASHBOARD_DATABASE_URL", f"sqlite:///{project_root / 'dashboard.db'}")
    
    print(f"Database: {db_url}")
    init_engine(db_url)
    
    # Create all tables (will skip existing ones)
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    
    print("[OK] Migration complete!")
    print("   Added tables: actions, llm_analyses")

if __name__ == "__main__":
    migrate()
