import pandas as pd
import os

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'
PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(RAW, 'Погода.xlsx'), skiprows=6, header=0)

df = df[['Местное время в Москве (ВДНХ)', 'T', 'Po', 'U', 'Ff', 'RRR']]
df.columns = ['Время', 'Температура', 'Давление', 'Влажность', 'Ветер', 'Осадки']

# Приводим числовые к числам
for col in ['Температура', 'Давление', 'Влажность', 'Ветер', 'Осадки']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['Время'] = pd.to_datetime(df['Время'], format='%d.%m.%Y %H:%M', errors='coerce')
df = df.dropna(subset=['Время'])
df['Дата'] = df['Время'].dt.date

daily = df.groupby('Дата').agg({
    'Температура': 'mean',
    'Давление': 'mean',
    'Влажность': 'mean',
    'Ветер': 'mean',
    'Осадки': 'sum'
}).reset_index()

daily['Дата'] = pd.to_datetime(daily['Дата'])
daily['Месяц'] = daily['Дата'].dt.to_period('M').astype(str)

print(daily.shape)
print(daily.head())

daily.to_excel(os.path.join(PROCESSED, 'Погода_дневная.xlsx'), index=False)
print('\nСохранено: Погода_дневная.xlsx')

# Агрегация по месяцам
monthly = daily.groupby('Месяц').agg({
    'Температура': 'mean',
    'Давление': 'mean',
    'Влажность': 'mean',
    'Ветер': 'mean',
    'Осадки': 'sum'
}).reset_index()

print('\nПо месяцам:')
print(monthly)

monthly.to_excel(os.path.join(PROCESSED, 'Погода_месячная.xlsx'), index=False)
print('\nСохранено: Погода_месячная.xlsx')