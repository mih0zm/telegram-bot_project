import sqlite3

def init_db():
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            username TEXT
        )
    ''')

    # Таблица расписания
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            date TEXT,
            time TEXT,
            teacher TEXT,
            link TEXT
        )
    ''')

    conn.commit()
    conn.close()

def add_user(chat_id, username):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (chat_id, username) VALUES (?, ?)', (chat_id, username))
    conn.commit()
    conn.close()