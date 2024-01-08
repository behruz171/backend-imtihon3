import sqlite3 as sq

async def db_connect():
    global db, curson
    db = sq.connect("database.db")
    curson = db.cursor()
    curson.execute('''
        CREATE TABLE IF NOT EXISTS users (
            users_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            age TEXT,
            email TEXT
        )
    ''')
    db.commit()

async def insert(name, phone, age, email):
    curson.execute(f"""
        INSERT INTO users(name, phone, age, email) VALUES ('{name}', '{phone}', '{age}', '{email}')
    """)
    db.commit()

def select():
    return curson.execute('''
        SELECT users_id, name FROM users;
    ''')