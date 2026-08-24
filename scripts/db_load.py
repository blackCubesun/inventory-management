import sqlite3
import pandas as pd
import os

DB_PATH = r'C:\Users\92585\Desktop\Sklad_System\data\sklad.db'
PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

conn = sqlite3.connect(DB_PATH)

df_ost = pd.read_excel(os.path.join(PROCESSED, 'Остатки_плоский.xlsx'))
df_god = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_год_плоский.xlsx'))
df_cena = pd.read_excel(os.path.join(PROCESSED, 'Цена_плоский.xlsx'))

# Чистим от мусора
for df in [df_ost, df_god, df_cena]:
    df = df[df['Код'].notna()]
    df = df[~df['Код'].astype(str).str.contains('Итого', na=False)]

df_ost.to_sql('Остатки', conn, if_exists='replace', index=False)
df_god.to_sql('РасходГод', conn, if_exists='replace', index=False)
df_cena.to_sql('Цены', conn, if_exists='replace', index=False)

conn.close()

print('Данные загружены')
print('Остатки:', df_ost.shape)
print('РасходГод:', df_god.shape)
print('Цены:', df_cena.shape)