import pandas as pd
import os
import re

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'
PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(RAW, 'Пробег.xlsx'), skiprows=5, header=0)
df = df.dropna(subset=['Автомобиль'])
df = df[df['Владелец'] == 'ГУП "Мосгортранс"'].copy()

# Извлекаем модель
def extract_model(s):
    s = str(s).upper()
    match = re.search(r'(КАМАЗ|НЕФАЗ)\s+(\d{4})', s)
    if match:
        return f'{match.group(1)} {match.group(2)}'
    return 'Другое'

df['Модель'] = df['Автомобиль'].apply(extract_model)

# Извлекаем дату ТО
def extract_date(s):
    if pd.isna(s):
        return None
    match = re.search(r'от (\d{2}\.\d{2}\.\d{4})', str(s))
    if match:
        return match.group(1)
    return None

df['ДатаТО'] = df['Последнее ТО'].apply(extract_date)
df['ДатаТО'] = pd.to_datetime(df['ДатаТО'], format='%d.%m.%Y', errors='coerce')
df['Месяц'] = df['ДатаТО'].dt.to_period('M').astype(str)

# Числовые
df['Пробег в день'] = pd.to_numeric(df['Пробег в день'], errors='coerce')

# Оставляем только транспорт
df = df[df['Модель'] != 'Другое']

# Сводная: месяц × модель → средний пробег в день
pivot = df.pivot_table(
    index='Месяц',
    columns='Модель',
    values='Пробег в день',
    aggfunc='mean'
).round(2)

print(pivot)
pivot.to_excel(os.path.join(PROCESSED, 'Пробег_динамика.xlsx'))
print('\nСохранено: Пробег_динамика.xlsx')