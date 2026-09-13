import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'
V2_PATH = os.path.join(PROCESSED, 'Модель_v2.xlsx')

# Загружаем плоские
df_ost = pd.read_excel(os.path.join(PROCESSED, 'Остатки_плоский.xlsx'))
df_rashod = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_год_плоский.xlsx'))
df_mes = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_месяц_плоский.xlsx'))
df_rez = pd.read_excel(os.path.join(PROCESSED, 'Резервы_плоский.xlsx'))
df_vp = pd.read_excel(os.path.join(PROCESSED, 'ВПути_плоский.xlsx'))

# Собираем уникальные СТО+Код
keys = []
for df in [df_ost, df_rashod, df_mes, df_rez, df_vp]:
    tmp = df[['СТО', 'Код']].copy()
    tmp['Код'] = tmp['Код'].astype(str).str.zfill(8)
    keys.append(tmp)

df_keys = pd.concat(keys, ignore_index=True).drop_duplicates()

# Добавляем SKN, Артикул, Наименование
info = df_ost[['Код', 'SKN', 'Артикул', 'Наименование']].copy()
info['Код'] = info['Код'].astype(str).str.zfill(8)
info = info.drop_duplicates(subset=['Код'])

df_keys = df_keys.merge(info, on='Код', how='left')

print(f'Ключей: {len(df_keys)}')
print(df_keys.head())

df_keys.to_excel(os.path.join(PROCESSED, '_Ключи_v2.xlsx'), index=False)
print('\nСохранено: _Ключи_v2.xlsx')