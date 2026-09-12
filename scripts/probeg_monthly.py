import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, 'Пробег_с_датами.xlsx'))

# Убираем время из дат
df['ДатаТО'] = pd.to_datetime(df['ДатаТО']).dt.date
df = df[df['ДатаНачала'] >= pd.Timestamp('2010-01-01')]

# Генерируем строки по месяцам для каждой машины
rows = []
for _, row in df.iterrows():
    # Месяцы от начала до ТО
    months = pd.date_range(start=row['ДатаНачала'], end=row['ДатаТО'], freq='MS')
    for m in months:
        rows.append({
            'Модель': row['Модель'],
            'Автомобиль': row['Автомобиль'],
            'Месяц': m.strftime('%Y-%m'),
            'ПробегВДень': row['Пробег в день']
        })

df_monthly = pd.DataFrame(rows)
print(f'Строк: {len(df_monthly)}')

# Агрегация: средний пробег в день по месяцам и моделям
pivot = df_monthly.pivot_table(
    index='Месяц',
    columns='Модель',
    values='ПробегВДень',
    aggfunc='mean'
).round(2)

print(pivot.tail(20))
pivot.to_excel(os.path.join(PROCESSED, 'Пробег_динамика.xlsx'))
print('\nСохранено: Пробег_динамика.xlsx')