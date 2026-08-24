import sqlite3
import os

DB_PATH = r'C:\Users\92585\Desktop\Sklad_System\data\sklad.db'

# Подключаемся (если файла нет — создастся)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Создаём таблицы
cursor.execute('''
CREATE TABLE IF NOT EXISTS Остатки (
    Код TEXT,
    SKN TEXT,
    Артикул TEXT,
    Наименование TEXT,
    СТО TEXT,
    Остаток REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS РасходГод (
    Код TEXT,
    SKN TEXT,
    Артикул TEXT,
    Наименование TEXT,
    СТО TEXT,
    Месяц TEXT,
    Расход REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Цены (
    Код TEXT,
    SKN TEXT,
    Артикул TEXT,
    Наименование TEXT,
    Цена REAL
)
''')

conn.commit()
conn.close()

print('База создана:', DB_PATH)