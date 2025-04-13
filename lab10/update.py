import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="ваша_база",
    user="ваш_пользователь",
    password="ваш_пароль",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# SQL-запрос на вставку данных
insert_query = "INSERT INTO phonebook (username, phone) VALUES (%s, %s);"
data = [
    ("Анна", "2345678901"),
    ("Пётр", "3456789012"),
    ("Ольга", "4567890123")
]

cursor.executemany(insert_query, data)
conn.commit()

print("Данные успешно добавлены.")

cursor.close()
conn.close()
