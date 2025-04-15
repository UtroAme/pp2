import psycopg2
import csv
from config import load_config


def insert_from_console():
    #Добовляем данные с консоли
    username = input("Enter username: ") #запрос имени и номера
    phone = input("Enter phone number: ")
    with psycopg2.connect(**load_config()) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone)) #ввод данных
        conn.commit()                                                  #%s - место куда будет поставленно значение

def insert_from_csv(filename='lab10/phonebook/contacts.csv'):
    #добавление c сsv файла
    with psycopg2.connect(**load_config()) as conn:
        with conn.cursor() as cur, open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (row[0], row[1]))
        conn.commit()

def update_entry():
    #обновление данных
    old_name = input("Enter current username to update: ")
    new_name = input("Enter new username (leave blank to skip): ")
    new_phone = input("Enter new phone (leave blank to skip): ")
    with psycopg2.connect(**load_config()) as conn:
        with conn.cursor() as cur:
            if new_name:
                cur.execute("UPDATE phonebook SET username = %s WHERE username = %s", (new_name, old_name))
            if new_phone:
                cur.execute("UPDATE phonebook SET phone = %s WHERE username = %s", (new_phone, new_name or old_name))
        conn.commit()

def query_data():
    #поиск по имени или по номеру
    with psycopg2.connect(**load_config()) as conn:
        with conn.cursor() as cur:
            choice = input("Filter by: 1 - name, 2 - phone: ")
            if choice == '1':
              name = input("Enter the name: ")
              cur.execute("SELECT * FROM phonebook WHERE username = %s", (name,))
            elif choice == '2':
              phone = input("Enterthe phone: ")
              cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
            for row in cur.fetchall():
              print(row)

def delete_entry():
    #удаление через имя или номер
    key = input("Delete by username or phone: ")
    with psycopg2.connect(**load_config()) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM phonebook
                WHERE username = %s OR phone = %s
            """, (key, key))
        conn.commit()

def main():
    while True:
        print("\nMenu:")
        print("1. Insert from console")
        print("2. Insert from CSV")
        print("3. Update entry")
        print("4. Query entries")
        print("5. Delete entry")
        print("6. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            insert_from_console()
        elif choice == '2':
            insert_from_csv()
        elif choice == '3':
            update_entry()
        elif choice == '4':
            query_data()
        elif choice == '5':
            delete_entry()
        elif choice == '6':
            break
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    main()
