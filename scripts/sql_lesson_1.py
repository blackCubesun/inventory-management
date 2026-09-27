import sqlite3
import pandas as pd

DB_PATH = r'C:\Users\92585\Desktop\Sklad_System\data\sklad.db'

conn = sqlite3.connect(DB_PATH)

query = """
SELECT СТО, Код, Наименование, ОстатокСТО, Зона
FROM Модель
WHERE СТО = 'Подразделение 13Э (Митино)'
  AND Зона = 'Крит'
LIMIT 10;
"""

df = pd.read_sql(query, conn)
print(df)

conn.close()