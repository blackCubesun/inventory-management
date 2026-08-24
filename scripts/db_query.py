import sqlite3
import pandas as pd

DB_PATH = r'C:\Users\92585\Desktop\Sklad_System\data\sklad.db'

conn = sqlite3.connect(DB_PATH)

# Запрос: остатки по каждой СТО
query1 = '''
SELECT СТО, COUNT(*) as Позиций, SUM(Остаток) as ВсегоОстаток
FROM Остатки
GROUP BY СТО
ORDER BY ВсегоОстаток DESC
'''

df1 = pd.read_sql(query1, conn)

# Запрос: топ-10 позиций по расходу за год
query2 = '''
SELECT Код, Наименование, SUM(Расход) as РасходГод
FROM РасходГод
GROUP BY Код, Наименование
ORDER BY РасходГод DESC
LIMIT 10
'''

df2 = pd.read_sql(query2, conn)

conn.close()

print('=== Остатки по СТО ===')
print(df1.head(10))

print('\n=== Топ-10 по расходу ===')
print(df2)