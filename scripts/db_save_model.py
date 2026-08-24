import sqlite3
import pandas as pd
import os

DB_PATH = r'C:\Users\92585\Desktop\Sklad_System\data\sklad.db'
PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем модель
df = pd.read_excel(os.path.join(PROCESSED, 'Модель.xlsx'))

# Чистим мусор
df = df[df['Код'].notna()]
df = df[~df['Код'].astype(str).str.contains('Итого', na=False)]

# Подключаемся к базе
conn = sqlite3.connect(DB_PATH)

# Сохраняем в таблицу Модель
df.to_sql('Модель', conn, if_exists='replace', index=False)

conn.close()

print('Модель сохранена в базу')
print('Строк:', df.shape[0])
print('Столбцов:', df.shape[1])