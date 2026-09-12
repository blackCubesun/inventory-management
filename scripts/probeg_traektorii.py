import pandas as pd
import os
import re

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'
PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(RAW, 'Пробег.xlsx'), skiprows=5, header=0)
df = df.dropna(subset=['Автомобиль'])
df = df[df['Владелец'] == 'ГУП "Мосгортранс"'].copy()

def extract_model(s):
    s = str(s).upper()
    match = re.search(r'(КАМАЗ|НЕФАЗ)\s+(\d{4})', s)
    if match:
        return f'{match.group(1)} {match.group(2)}'
    return 'Другое'

df['Модель'] = df['Автомобиль'].apply(extract_model)

def extract_date(s):
    if pd.isna(s):
        return None
    match = re.search(r'от (\d{2}\.\d{2}\.\d{4})', str(s))
    if match:
        return match.group(1)
    return None

df['ДатаТО'] = df['Последнее ТО'].apply(extract_date)
df['ДатаТО'] = pd.to_datetime(df['ДатаТО'], format='%d.%m.%Y', errors='coerce')

for col in ['Начальный пробег', 'Пробег', 'Конечный пробег', 'Пробег в день']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df[df['Модель'] != 'Другое']
df = df.dropna(subset=['Конечный пробег', 'Пробег в день', 'ДатаТО'])

# Фильтруем аномалии
df = df[(df['Пробег в день'] >= 10) & (df['Пробег в день'] <= 500)]
df = df[(df['Конечный пробег'] >= 100) & (df['Конечный пробег'] <= 1000000)]

# Восстанавливаем дату начала
df['ДнейВЭксплуатации'] = df['Конечный пробег'] / df['Пробег в день']
df['ДатаНачала'] = df['ДатаТО'] - pd.to_timedelta(df['ДнейВЭксплуатации'], unit='D')
df = df[df['ДнейВЭксплуатации'] <= 365 * 15]  # не больше 15 лет

print(f'Машин после фильтра: {len(df)}')
print(f'\nТоп-10:')
print(df[['Модель', 'Конечный пробег', 'Пробег в день', 'ДатаТО', 'ДатаНачала']].head(10))

df.to_excel(os.path.join(PROCESSED, 'Пробег_с_датами.xlsx'), index=False)
print('\nСохранено: Пробег_с_датами.xlsx')