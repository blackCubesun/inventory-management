import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем данные
df_probeg = pd.read_excel(os.path.join(PROCESSED, 'Пробег_динамика.xlsx'))
df_pogoda = pd.read_excel(os.path.join(PROCESSED, 'Погода_месячная.xlsx'))
df_models = pd.read_excel(os.path.join(PROCESSED, 'Справочник_Модели.xlsx'))

# Считаем количество машин по моделям
df_dates = pd.read_excel(os.path.join(PROCESSED, 'Пробег_с_датами.xlsx'))
kolvo = df_dates['Модель'].value_counts().reset_index()
kolvo.columns = ['Модель', 'КолМашин']
print('Машин по моделям:')
print(kolvo)

# Переводим в long-формат
df_long = df_probeg.melt(id_vars='Месяц', var_name='Модель', value_name='ПробегВДень')
df_long = df_long.dropna()

# Соединяем с погодой
df_long = df_long.merge(df_pogoda[['Месяц', 'Температура']], on='Месяц', how='left')

# Соединяем с моделями
df_long = df_long.merge(df_models[['Модель', 'Тип', 'РасходЛетоМин', 'РасходЗимаМин']], on='Модель', how='left')

# Количество машин
df_long = df_long.merge(kolvo, on='Модель', how='left')

# Определяем сезон: если температура < 5 — зима
df_long['РасходНаКм'] = df_long.apply(
    lambda r: r['РасходЗимаМин'] if r['Температура'] < 5 else r['РасходЛетоМин'],
    axis=1
)

# Дней в месяце
df_long['Месяц_dt'] = pd.to_datetime(df_long['Месяц'])
df_long['ДнейВМесяце'] = df_long['Месяц_dt'].dt.days_in_month

# Пробег за месяц = пробег в день × дни × количество машин
df_long['ПробегЗаМесяц'] = df_long['ПробегВДень'] * df_long['ДнейВМесяце'] * df_long['КолМашин']

# Потребление
df_long['Потребление'] = df_long['ПробегЗаМесяц'] * df_long['РасходНаКм']

# Суммарное потребление по месяцам
total = df_long.groupby('Месяц')['Потребление'].sum()
print(total.tail(12))

print('\nПример:')
print(df_long[['Месяц', 'Модель', 'ПробегВДень', 'Температура', 'РасходНаКм', 'Потребление']].tail(10))

df_long.to_excel(os.path.join(PROCESSED, 'Потребление.xlsx'), index=False)
print('\nСохранено: Потребление.xlsx')