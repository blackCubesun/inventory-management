import sqlite3
conn = sqlite3.connect(r'C:\Users\92585\Desktop\Sklad_System\data\sklad.db')
cursor = conn.execute('PRAGMA table_info(Модель)')
for row in cursor:
    print(row[1])
conn.close()