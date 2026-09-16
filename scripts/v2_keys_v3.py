import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем все плоские
df_ost = pd.read_excel(os.path.join(PROCESSED, 'Остатки_плоский.xlsx'))
df_rashod = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_год_плоский.xlsx'))
df_mes = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_месяц_плоский.xlsx'))
df_rez = pd.read_excel(os.path.join(PROCESSED, 'Резервы_плоский_испр.xlsx'))
df_vp = pd.read_excel(os.path.join(PROCESSED, 'ВПути_плоский.xlsx'))

# Приводим Коды к тексту
for df in [df_ost, df_rashod, df_mes, df_rez, df_vp]:
    df['Код'] = df['Код'].astype(str).str.zfill(8)

# Собираем ключи
keys = []
for df in [df_ost, df_rashod, df_mes, df_rez, df_vp]:
    tmp = df[['СТО', 'Код']].copy()
    keys.append(tmp)

df_keys = pd.concat(keys, ignore_index=True).drop_duplicates()

# Собираем ВСЮ информацию о товарах из всех таблиц
info_list = []
for df in [df_ost, df_rashod, df_mes, df_rez, df_vp]:
    if 'Артикул' in df.columns and 'Наименование' in df.columns:
        tmp = df[['Код', 'SKN', 'Артикул', 'Наименование']].copy()
        info_list.append(tmp)

info_all = pd.concat(info_list, ignore_index=True)
info_all = info_all.dropna(subset=['Артикул'])
info_all = info_all.drop_duplicates(subset=['Код'], keep='first')

print(f'Уникальных товаров с информацией: {len(info_all)}')

# Соединяем
df_keys = df_keys.merge(info_all, on='Код', how='left')

print(f'\nКлючей: {len(df_keys)}')
print(f'Артикул пустой: {df_keys["Артикул"].isna().sum()}')
print(f'Наименование пустое: {df_keys["Наименование"].isna().sum()}')

df_keys.to_excel(os.path.join(PROCESSED, '_Ключи_v3.xlsx'), index=False)
print('\nСохранено: _Ключи_v3.xlsx')