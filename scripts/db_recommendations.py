import sqlite3
import pandas as pd

DB_PATH = r'C:\Users\92585\Desktop\Sklad_System\data\sklad.db'

conn = sqlite3.connect(DB_PATH)

sto_name = 'Подразделение 10А (Марьина Роща)'

# 1. Переместить с ЦС
query_cs = f'''
SELECT Код, SKN, Наименование, ОстатокСТО, ДефицитДоЦели, СвободноЦС, НужноПереместить
FROM Модель
WHERE СТО = '{sto_name}'
  AND Зона = 'Крит'
  AND НужноПереместить > 0
ORDER BY НужноПереместить DESC
LIMIT 20
'''

# 2. Излишки на других СТО
query_izl = f'''
SELECT m.Код, m.SKN, m.СТО, m.Наименование, m.ИзлишекСверхЦели
FROM Модель m
WHERE m.Зона = 'Избыток'
  AND m.СТО != '{sto_name}'
  AND m.ИзлишекСверхЦели > 0
  AND m.Код IN (
      SELECT Код FROM Модель
      WHERE СТО = '{sto_name}' AND Зона = 'Крит'
  )
ORDER BY m.ИзлишекСверхЦели DESC
LIMIT 20
'''

df_cs = pd.read_sql(query_cs, conn)
df_izl = pd.read_sql(query_izl, conn)

conn.close()

print(f'=== ПЕРЕМЕСТИТЬ С ЦС ({len(df_cs)} позиций) ===')
print(df_cs.head(10))

print(f'\n=== ИЗЛИШКИ НА ДРУГИХ СТО ({len(df_izl)} позиций) ===')
print(df_izl.head(10))