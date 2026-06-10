from database import create_database_if_not_exists, create_table, insert_sample_data


def main():
    print("Initializing PostgreSQL database...")
    create_database_if_not_exists()
    print("Database ready.")
    create_table()
    print("Table created or already exists.")
    insert_sample_data()
    print("Sample data inserted.")
    print("Initialization complete.")


if __name__ == "__main__":
    main()
