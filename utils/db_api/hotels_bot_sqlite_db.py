import sqlite3
from typing import Dict, List

from loguru import logger

conn = sqlite3.connect('hotels_bot_db.db')
conn.execute("PRAGMA foreign_keys = 0")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    f_name TEXT,
    l_name TEXT,
    user_name TEXT
)
""")

conn.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages(
    message_id INTEGER PRIMARY KEY,
    command TEXT,
    created_at TIMESTAMP,
    city_name TEXT,
    hotels_amount INT,
    photo_amount INT default 0,
    max_price REAL DEFAULT 0.0,
    distance_from_center REAL default 0,
    check_in TEXT,
    check_out TEXT,
    adults_qnt INT DEFAULT 0,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
""")

conn.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS hotels(
    id INTEGER PRIMARY KEY, 
    hotel_id INTEGER,
    hotel_name TEXT,
    address TEXT,
    distance_from_center REAL DEFAULT 0.00,
    price TEXT,
    message_id INTEGER,
    FOREIGN KEY (message_id) REFERENCES messages(message_id) 
)
""")

conn.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS photos(
    id INTEGER PRIMARY KEY ,
    photo_url TEXT,
    hotel_id INTEGER,
    FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
    )
""")


def insert(table: str, column_values: Dict):
    """
    Добавляет данные в базу данных
    :param table: Таблица в которую необходимо добавить.
    :param column_values: Поле и значение передаем словарем.
    :return:
    """
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholder = ', '.join('?' * len(column_values.keys()))
    cursor.executemany(
        f'INSERT OR REPLACE INTO {table}'
        f'({columns})'
        f'VALUES ({placeholder})', values)

    conn.commit()
    logger.info('Данные пользователя добавлены в базу данных')


def fetch_all(table: str, columns: List[str], detail: str = '') -> List[dict]:
    columns_joined = ', '.join(columns)
    cursor.execute(
        f'SELECT {columns_joined} FROM {table} WHERE {detail} ORDER BY message_id DESC') if detail != '' else cursor.execute(
        f'SELECT {columns_joined} FROM {table} ORDER BY message_id DESC')
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result
