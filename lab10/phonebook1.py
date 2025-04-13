import psycopg2
import csv
from configparser import ConfigParser

# --- Database connection functions ---

def load_config(filename='lab10/database.ini', section='postgresql'):
    """
    Load database configuration parameters from an INI file.
    """
    parser = ConfigParser()
    parser.read(filename)
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for key, value in params:
            config[key] = value
    else:
        raise Exception(f'Section {section} not found in the {filename} file')
    return config

def get_db_connection():
    """
    Establish and return a database connection using parameters from the configuration file.
    """
    config = load_config()
    conn = psycopg2.connect(**config)
    return conn

def create_phonebook_table():
    """
    Creates the phonebook table if it doesn't exist.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


# --- Inserting data functions ---

def insert_data_from_csv(csv_filename):
    """
    Reads phonebook data from a CSV file and inserts it into the database.
    The CSV file should have headers: first_name,phone
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        with open(csv_filename, 'r', newline='', encoding='Windows-1251') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                first_name = row['first_name']
                phone = row['phone']
                cur.execute(
                    "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", 
                    (first_name, phone)
                )
        conn.commit()
        print("Data from CSV inserted successfully!")
    except Exception as e:
        print("Error inserting data from CSV:", e)
    finally:
        cur.close()
        conn.close()


def insert_data_from_console():
    """
    Prompts the user for input and inserts a new phonebook record.
    """
    first_name = input("Enter user name: ")
    phone = input("Enter phone: ")
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
            (first_name, phone)
        )
        conn.commit()
        print("Record inserted successfully!")
    except Exception as e:
        print("Error inserting record:", e)
    finally:
        cur.close()
        conn.close()


# --- Updating data functions ---

def update_user_data(username):
    """
    Updates either the first name or phone number for a given user (matched by first_name).
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        print("Choose the field to update:")
        print("1. Update First Name")
        print("2. Update Phone")
        choice = input("Enter choice (1 or 2): ")
    
        if choice == '1':
            new_first_name = input("Enter new first name: ")
            cur.execute(
                "UPDATE phonebook SET first_name = %s WHERE first_name = %s",
                (new_first_name, username)
            )
            print(f"First name updated from {username} to {new_first_name}.")
        elif choice == '2':
            new_phone = input("Enter new phone number: ")
            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE first_name = %s",
                (new_phone, username)
            )
            print(f"Phone updated for user {username}.")
        else:
            print("Invalid choice. No changes made.")
        conn.commit()
    except Exception as e:
        print("Error updating record:", e)
    finally:
        cur.close()
        conn.close()


# --- Querying data functions ---

def query_all_entries():
    """
    Queries and displays all records from the phonebook.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM phonebook")
        records = cur.fetchall()
        print("All entries in PhoneBook:")
        for record in records:
            print(record)
    except Exception as e:
        print("Error querying records:", e)
    finally:
        cur.close()
        conn.close()


def query_by_username(username):
    """
    Queries and displays phonebook records for an exact match of first_name.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM phonebook WHERE first_name = %s", (username,))
        records = cur.fetchall()
        if records:
            print("Records found:")
            for record in records:
                print(record)
        else:
            print("No records found with that username.")
    except Exception as e:
        print("Error querying by username:", e)
    finally:
        cur.close()
        conn.close()


def query_by_phone(phone):
    """
    Queries and displays phonebook records that match the given phone number.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
        records = cur.fetchall()
        if records:
            print("Records found:")
            for record in records:
                print(record)
        else:
            print("No records found with that phone number.")
    except Exception as e:
        print("Error querying by phone:", e)
    finally:
        cur.close()
        conn.close()


# --- Deleting data functions ---

def delete_by_username(username):
    """
    Deletes records from the phonebook table by matching first_name.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM phonebook WHERE first_name = %s", (username,))
        conn.commit()
        print(f"Deleted records for user: {username}")
    except Exception as e:
        print("Error deleting record:", e)
    finally:
        cur.close()
        conn.close()


# --- Main interactive menu ---

def main_menu():
    create_phonebook_table()  # Ensure the table exists before we proceed

    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from CSV")
        print("2. Insert from Console")
        print("3. Update a Record")
        print("4. Query All Entries")
        print("5. Query by Username")
        print("6. Query by Phone")
        print("7. Delete by Username")
        print("8. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            csv_file = input("Enter CSV file name (with path if needed): ")
            insert_data_from_csv(csv_file)
        elif choice == '2':
            insert_data_from_console()
        elif choice == '3':
            username = input("Enter the username whose record you want to update: ")
            update_user_data(username)
        elif choice == '4':
            query_all_entries()
        elif choice == '5':
            username = input("Enter username to search: ")
            query_by_username(username)
        elif choice == '6':
            phone = input("Enter phone to search: ")
            query_by_phone(phone)
        elif choice == '7':
            username = input("Enter username to delete: ")
            delete_by_username(username)
        elif choice == '8':
            print("Exiting PhoneBook. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == '__main__':
    main_menu()
