import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем
df = pd.read_excel(os.path.join(PROCESSED, 'ML_РасходПоТипам.xlsx'))
df['Дата'] = pd.to_datetime(df['Дата'])
df['Месяц'] = df['Дата'].dt.to_period('M').astype(str)

# Погода
df_pogoda = pd.read_excel(os.path.join(PROCESSED, 'Погода_месячная.xlsx'))
df_pogoda.columns = ['Месяц', 'Температура', 'Давление', 'Влажность', 'Ветер', 'Осадки']

# Потребление
df_potr = pd.read_excel(os.path.join(PROCESSED, 'Потребление.xlsx'))
df_potr_total = df_potr.groupby('Месяц')['Потребление'].sum().reset_index()
df_potr_total.columns = ['Месяц', 'ПотреблениеТоплива']

# Соединяем
df = df.merge(df_pogoda, on='Месяц', how='left')
df = df.merge(df_potr_total, on='Месяц', how='left')

# Признаки времени
df['Год'] = df['Дата'].dt.year
df['НомерМесяца'] = df['Дата'].dt.month

# Сортируем
df = df.sort_values(['Код', 'ТипСТО', 'Дата'])

# Лаги по Код + ТипСТО
df['Расход_Лаг1'] = df.groupby(['Код', 'ТипСТО'])['Расход'].shift(1)
df['Расход_Лаг12'] = df.groupby(['Код', 'ТипСТО'])['Расход'].shift(12)
df['Расход_Среднее3'] = df.groupby(['Код', 'ТипСТО'])['Расход'].transform(
    lambda x: x.rolling(3, min_periods=1).mean()
)

print(df.head(20))
print(f'\nРазмер: {df.shape}')
print(f'Столбцы: {list(df.columns)}')

df.to_excel(os.path.join(PROCESSED, 'ML_Dataset_v2.xlsx'), index=False)
print('\nСохранено: ML_Dataset_v2.xlsx')