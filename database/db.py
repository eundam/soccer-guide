import duckdb

DB_PATH = "soccer_guide.db"

def get_connection():
    return duckdb.connect(DB_PATH)