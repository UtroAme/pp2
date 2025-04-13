import csv 
import psycopg2
from config import load_config
from configparser import ConfigParser

'''Connecting'''
def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

'''config'''
def load_config(filename='lab10/database.ini', section='postgresql'):
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

'''Creating the table of PhoneBook'''
def create_phonebook_table():
    #создает таблицу если ее нет 
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL
    );
"""
    try:
      config = load_config()
      with psycopg2.connect(**config) as conn:
         with conn.cursor() as cur:
            cur.execute(create_table_sql)
         conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

#Вставка даных из CSV файла
def insert_data_from_csv(csv_file_path):
   #чтение данных из cvs вставка в таблицу
    config = load_config()
    insert_sql = "INSERT INTO phonebook(username, phone) VALUES (%s, %s);"
    try:
       cur = conn.cursor()
       with open(csv_file_path, 'r', newline='', encoding='Windows-1251') as csvfile:
          reader = csv.DictReader(csvfile)
          for row in reader:
            first_name = row['first_name']
            phone = row['phone']
            cur.execute("INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)", 
                        (first_name, phone))
       with psycopg2.connect(**config) as conn:
            conn.commit()
    except Exception as error:
       print(error)

#Вставка данных с консоли
def insert_data_from_console():
    #запрос от пользователя имени и телефона полсе втсавка
    username = input("Введите имя пользователя: ").strip()
    phone = input("Введите номер телефона: ").strip()
    config = load_config()
    insert_sql = "INSERT INTO phonebook(username, phone) VALUES (%s, %s) RETURNING id;"
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(insert_sql, (username, phone))
                inserted_id = cur.fetchone()[0]
            conn.commit()
            print(f"Запись успешно добавлена с ID {inserted_id}.")
    except Exception as error:
        print(error)

#обновленние данных
def update_contact(old_username, new_username=None, new_phone=None):
    """
    Обновление записи контакта по старому имени.
    Можно изменить либо имя, либо телефон, либо оба поля.
    """
    if not (new_username or new_phone):
        print("Нужно предоставить новое имя или номер телефона для обновления!")
        return

    # Формируем SQL запрос динамически
    set_statements = []
    values = []
    if new_username:
        set_statements.append("username = %s")
        values.append(new_username)
    if new_phone:
        set_statements.append("phone = %s")
        values.append(new_phone)
    set_clause = ", ".join(set_statements)
    update_sql = f"UPDATE phonebook SET {set_clause} WHERE username = %s;"
    values.append(old_username)
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(update_sql, tuple(values))
            conn.commit()
            print(f"Обновлено строк: {cur.rowcount}")
    except Exception as error:
        print(error)

#выбор с филтрами 
def query_contacts(filter_by=None, filter_value=None):
    #Выборка данных из таблицы phonebook с опциональным фильтром.
    #:param filter_by: может быть 'username' или 'phone'
    #:param filter_value: значение для фильтрации (например, 'John' или '123')

    config = load_config()
    base_sql = "SELECT id, username, phone FROM phonebook"
    if filter_by and filter_value:
        base_sql += f" WHERE {filter_by} ILIKE %s"  # ILIKE для нечувствительного к регистру поиска
        params = (f"%{filter_value}%",)
    else:
        params = None
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(base_sql, params)
                rows = cur.fetchall()
                if rows:
                    print("Результаты запроса:")
                    for row in rows:
                        print(f"ID: {row[0]}, Имя: {row[1]}, Телефон: {row[2]}")
                else:
                    print("Нет данных для отображения.")
    except Exception as error:
        print(error)

#Удаления данных по имени 
def delete_contact(username):
    #Удаление записи из phonebook по имени пользователя.
    config = load_config()
    delete_sql = "DELETE FROM phonebook WHERE username = %s;"
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(delete_sql, (username,))
                conn.commit()
                print(f"Удалено строк: {cur.rowcount}")
    except Exception as error:
        print(error)

#Меню
def main_menu():
    create_phonebook_table()  # Создаем таблицу, если её еще нет

    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Вставка данных из CSV файла")
        print("2. Вставка данных с консоли")
        print("3. Обновить запись")
        print("4. Вывести все контакты / Поиск")
        print("5. Удалить запись по имени")
        print("6. Выход")
        choice = input("Выберите действие (1-6): ").strip()

        if choice == '1':
            csv_file = input("Введите путь к CSV файлу: ").strip()
            insert_data_from_csv(csv_file)
        elif choice == '2':
            insert_data_from_console()
        elif choice == '3':
            old_name = input("Введите текущее имя контакта для обновления: ").strip()
            new_name = input("Введите новое имя (оставьте пустым, если не менять): ").strip()
            new_phone = input("Введите новый номер телефона (оставьте пустым, если не менять): ").strip()
            # Передаем None, если поле пустое
            update_contact(old_name, new_username=new_name if new_name else None, new_phone=new_phone if new_phone else None)
        elif choice == '4':
            print("Фильтр: ")
            print("1. Без фильтра")
            print("2. По имени")
            print("3. По номеру телефона")
            filter_choice = input("Ваш выбор (1-3): ").strip()
            if filter_choice == '1':
                query_contacts()
            elif filter_choice == '2':
                name_filter = input("Введите часть имени для поиска: ").strip()
                query_contacts("username", name_filter)
            elif filter_choice == '3':
                phone_filter = input("Введите часть номера для поиска: ").strip()
                query_contacts("phone", phone_filter)
            else:
                print("Неверный выбор.")
        elif choice == '5':
            del_name = input("Введите имя контакта для удаления: ").strip()
            delete_contact(del_name)
        elif choice == '6':
            print("Выход из приложения.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == '__main__':
    create_phonebook_table()
    main_menu()
