import psycopg2
import json

# ---------- DATABASE CONFIG ----------
DB_CONFIG = {
    "dbname": "your_database_name",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}


def create_table(conn):
    """Create table if it doesn't already exist."""
    create_query = """
    CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        doc_attributes JSONB NOT NULL DEFAULT '{}'
    );
    """
    with conn.cursor() as cur:
        cur.execute(create_query)
    conn.commit()


def upsert_document(conn, doc_id, attributes: dict):
    """Insert or update document attributes (merge JSONB keys)."""
    upsert_query = """
        INSERT INTO documents (doc_id, doc_attributes)
        VALUES (%s, %s::jsonb)
        ON CONFLICT (doc_id)
        DO UPDATE
        SET doc_attributes = documents.doc_attributes || EXCLUDED.doc_attributes;
    """
    with conn.cursor() as cur:
        cur.execute(upsert_query, (doc_id, json.dumps(attributes)))
    conn.commit()


def get_attributes(conn, doc_id):
    """Fetch doc_attributes by doc_id and return as Python dict."""
    select_query = "SELECT doc_attributes FROM documents WHERE doc_id = %s;"
    with conn.cursor() as cur:
        cur.execute(select_query, (doc_id,))
        row = cur.fetchone()
        if row:
            return row[0]  # JSONB automatically converts to dict in psycopg2
        else:
            return None


# ---------- MAIN EXECUTION ----------
if __name__ == "__main__":
    conn = psycopg2.connect(**DB_CONFIG)

    # Step 1: Ensure table exists
    create_table(conn)

    # Step 2: Example upserts
    upsert_document(conn, "doc_1", {"name": "Gopi", "age": 25})
    upsert_document(conn, "doc_1", {"age": 26, "location": "Chennai"})

    # Step 3: Get attributes by doc_id
    data = get_attributes(conn, "doc_1")
    print("Fetched attributes:", data)

    conn.close()
