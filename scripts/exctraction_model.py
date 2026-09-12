import pandas as pd
import os
import re

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'
PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(RAW, 'Пробег.xlsx'), skiprows=5, header=0)
df = df.dropna(subset=['Автомобиль'])

# Только Мосгортранс
df = df[df['Владелец'] == 'ГУП "Мосгортранс"'].copy()

# Извлекаем марку
def extract_marka(s):
    s = str(s).upper()
    for marka in ['КАМАЗ', 'НЕФАЗ', 'УБЗС', 'ЛИАЗ', 'ВОЛГАБАС']:
        if marka in s:
            return marka
    return 'Другое'

df['Марка'] = df['Автомобиль'].apply(extract_marka)

print('Машин по маркам:')
print(df['Марка'].value_counts())

# Приводим числовые столбцы
for col in ['Начальный пробег', 'Пробег', 'Конечный пробег', 'Пробег в день']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Средний пробег по маркам
print('=== Средний пробег по маркам ===')
stats = df.groupby('Марка').agg({
    'Пробег': 'mean',
    'Пробег в день': 'mean',
    'Конечный пробег': 'mean',
    'Автомобиль': 'count'
}).round(2)
stats.columns = ['СреднийПробег', 'СреднийВДень', 'СреднийОбщий', 'КолМашин']
print(stats)

import re

def extract_model(s):
    s = str(s).upper()
    # Ищем цифры после марки
    match = re.search(r'(КАМАЗ|НЕФАЗ)\s+(\d{4})', s)
    if match:
        return f'{match.group(1)} {match.group(2)}'
    return 'Другое'

df['Модель'] = df['Автомобиль'].apply(extract_model)

print('Модели:')
print(df['Модель'].value_counts())

df_transport = df[df['Модель'] != 'Другое'].copy()

stats = df_transport.groupby('Модель').agg({
    'Пробег': 'mean',
    'Пробег в день': 'mean',
    'Конечный пробег': 'mean',
    'Автомобиль': 'count'
}).round(2)
stats.columns = ['СреднийПробег', 'СреднийВДень', 'ОбщийПробег', 'КолМашин']
print(stats)