import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем расход
df = pd.read_excel(os.path.join(PROCESSED, 'ML_РасходПоМесяцам.xlsx'))
df['Дата'] = pd.to_datetime(df['Дата'])
df['Месяц'] = df['Дата'].dt.to_period('M').astype(str)

# Загружаем погоду
df_pogoda = pd.read_excel(os.path.join(PROCESSED, 'Погода_месячная.xlsx'))
df_pogoda.columns = ['Месяц', 'Температура', 'Давление', 'Влажность', 'Ветер', 'Осадки']

# Загружаем потребление
df_potr = pd.read_excel(os.path.join(PROCESSED, 'Потребление.xlsx'))
df_potr_total = df_potr.groupby('Месяц')['Потребление'].sum().reset_index()
df_potr_total.columns = ['Месяц', 'ПотреблениеТоплива']

# Соединяем
df = df.merge(df_pogoda, on='Месяц', how='left')
df = df.merge(df_potr_total, on='Месяц', how='left')

# Добавляем признаки времени
df['Год'] = df['Дата'].dt.year
df['НомерМесяца'] = df['Дата'].dt.month

# Сортируем
df = df.sort_values(['Код', 'Дата'])

# Лаг 1: расход за прошлый месяц
df['Расход_Лаг1'] = df.groupby('Код')['Расход'].shift(1)

# Лаг 12: расход за тот же месяц год назад
df['Расход_Лаг12'] = df.groupby('Код')['Расход'].shift(12)

# Средний расход за 3 месяца
df['Расход_Среднее3'] = df.groupby('Код')['Расход'].transform(lambda x: x.rolling(3, min_periods=1).mean())

print(df.head(20))
print(f'\nРазмер: {df.shape}')
print(f'Столбцы: {list(df.columns)}')

df.to_excel(os.path.join(PROCESSED, 'ML_Dataset.xlsx'), index=False)
print('\nСохранено: ML_Dataset.xlsx')