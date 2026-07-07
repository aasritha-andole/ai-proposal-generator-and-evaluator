from database.db import get_connection

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proposals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idea TEXT,
        agency TEXT,
        title TEXT,
        abstract TEXT,
        methodology TEXT,
        timeline TEXT,
        embedding TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proposal_id INTEGER,
        personnel_cost REAL,
        equipment_cost REAL,
        software_cost REAL,
        misc_cost REAL,
        total_budget REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proposal_id INTEGER,
        innovation_score REAL,
        feasibility_score REAL,
        clarity_score REAL,
        final_score REAL
    )
    """)

    conn.commit()
    conn.close()