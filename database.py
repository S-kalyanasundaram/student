import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def get_db_settings():
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "student_db"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres"),
    }


def get_connection(dbname=None):
    settings = get_db_settings()
    return psycopg2.connect(
        host=settings["host"],
        port=settings["port"],
        dbname=dbname or settings["dbname"],
        user=settings["user"],
        password=settings["password"],
    )


def create_database_if_not_exists():
    settings = get_db_settings()
    admin_conn = psycopg2.connect(
        host=settings["host"],
        port=settings["port"],
        dbname="postgres",
        user=settings["user"],
        password=settings["password"],
    )
    admin_conn.autocommit = True
    with admin_conn.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (settings["dbname"],),
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(settings["dbname"])))
    admin_conn.close()


def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS student_profile (
        id SERIAL PRIMARY KEY,
        name VARCHAR(26) NOT NULL,
        student_id VARCHAR(20) UNIQUE,
        relation_name VARCHAR(26),
        date_of_birth DATE,
        aadhaar_number VARCHAR(12) UNIQUE,
        city VARCHAR(100),
        pin_code VARCHAR(6),
        is_active BOOLEAN DEFAULT TRUE
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()


def insert_sample_data():
    sample_records = [
        (
            "Rahul Sharma",
            "STU1001",
            "Sunita Sharma",
            "2004-05-12",
            "123456789012",
            "Mumbai",
            "400001",
            True,
        ),
        (
            "Anita Singh",
            "STU1002",
            "Raj Singh",
            "2005-08-24",
            "234567890123",
            "Delhi",
            "110001",
            True,
        ),
    ]
    insert_sql = """
    INSERT INTO student_profile (name, student_id, relation_name, date_of_birth, aadhaar_number, city, pin_code, is_active)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (student_id) DO NOTHING;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            for record in sample_records:
                cursor.execute(insert_sql, record)
        conn.commit()


def add_student(name, student_id, relation_name, date_of_birth, aadhaar_number, city, pin_code, is_active):
    sql = """
    INSERT INTO student_profile (name, student_id, relation_name, date_of_birth, aadhaar_number, city, pin_code, is_active)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, student_id, relation_name, date_of_birth, aadhaar_number, city, pin_code, is_active))
            student_id_pk = cursor.fetchone()[0]
        conn.commit()
    return student_id_pk


def get_all_students():
    sql = "SELECT * FROM student_profile ORDER BY id;"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql)
            return cursor.fetchall()


def search_students(query, search_by="name"):
    field = "name" if search_by.lower() == "name" else "student_id"
    sql = f"SELECT * FROM student_profile WHERE {field} ILIKE %s ORDER BY id;"
    term = f"%{query.strip()}%"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, (term,))
            return cursor.fetchall()


def get_student_by_id(student_pk):
    sql = "SELECT * FROM student_profile WHERE id = %s;"
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql, (student_pk,))
            return cursor.fetchone()


def update_student(student_pk, name, student_id, relation_name, date_of_birth, aadhaar_number, city, pin_code, is_active):
    sql = """
    UPDATE student_profile
    SET name = %s,
        student_id = %s,
        relation_name = %s,
        date_of_birth = %s,
        aadhaar_number = %s,
        city = %s,
        pin_code = %s,
        is_active = %s
    WHERE id = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, student_id, relation_name, date_of_birth, aadhaar_number, city, pin_code, is_active, student_pk))
        conn.commit()


def delete_student(student_pk):
    sql = "DELETE FROM student_profile WHERE id = %s;"
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (student_pk,))
        conn.commit()
