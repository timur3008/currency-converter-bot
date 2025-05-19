import sqlite3
from pathlib import Path
from typing import Any
from datetime import datetime

BASE_PATH = Path(__name__).resolve().parent

def create_database() -> None:
    connection = sqlite3.connect(BASE_PATH / 'convertations.db')
    cursor = connection.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id BIGINT    
        );
                
        CREATE TABLE IF NOT EXISTS convertations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency_from VARCHAR(5),
            currency_to VARCHAR(5),
            original_num REAL,
            converted_num REAL,
            currency_from_symbol VARCHAR(3),
            currency_to_symbol VARCHAR(3),
            converted_at DATE,
            user_id INTEGER REFERENCES users(id)
        );
    ''')

    connection.commit()
    connection.close()

def add_user_to_database(chat_id: int) -> None:
    connection = sqlite3.connect(BASE_PATH / 'convertations.db')
    cursor = connection.cursor()
    create_database()
    query = 'INSERT INTO users(chat_id) VALUES (?);'
    cursor.execute(query, (chat_id,))

    connection.commit()
    connection.close()
    print(f'user with {chat_id=} was added')

def get_user_from_database(chat_id: int) -> tuple[Any] | None:
    connection = sqlite3.connect(BASE_PATH / 'convertations.db')
    cursor = connection.cursor()
    create_database()
    query = 'SELECT id FROM users WHERE chat_id = ?;'
    cursor.execute(query, (chat_id,))

    connection.commit()
    data = cursor.fetchone()
    connection.close()
    return data

def add_convertation(
        currency_from: str, 
        currency_to: str, 
        original_num: float, 
        converted_num: float, 
        from_symbol: str, 
        to_symbol: str, 
        converted_at: datetime, 
        chat_id: int) -> None:
    connection = sqlite3.connect(BASE_PATH / 'convertations.db')
    cursor = connection.cursor()

    user_id = get_user_from_database(chat_id=chat_id)[0]

    query = '''
        INSERT INTO convertations(currency_from, currency_to, original_num, converted_num, currency_from_symbol, currency_to_symbol, converted_at, user_id)
        VALUES (?,?,?,?,?,?,?,?);
    '''
    cursor.execute(query, (
        currency_from,
        currency_to,
        original_num,
        converted_num,
        from_symbol,
        to_symbol,
        converted_at,
        user_id
    ))
    connection.commit()
    connection.close()

def get_convertations(chat_id: int) -> list[Any]:
    connection = sqlite3.connect(BASE_PATH / 'convertations.db')
    cursor = connection.cursor()

    user_id = get_user_from_database(chat_id=chat_id)[0]
    cursor.execute(
        'SELECT * FROM convertations WHERE user_id = ?;',
        (user_id,)
    )

    connection.commit()
    return cursor.fetchall()
    