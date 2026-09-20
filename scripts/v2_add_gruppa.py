import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем Расчёт
df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_final.xlsx'))
df['Артикул'] = df['Артикул'].astype(str).str.strip()
df['Код'] = df['Код'].astype(str).str.zfill(8)

# Загружаем иерархию
df_ier = pd.read_excel(os.path.join(PROCESSED, 'Иерархия_товаров_укрупнённая.xlsx'))
df_ier['Артикул'] = df_ier['Артикул'].astype(str).str.strip()

print(f'Расчёт: {len(df)}')
print(f'Иерархия: {len(df_ier)}')

# Соединяем по Артикулу
df = df.merge(
    df_ier[['Артикул', 'Родитель', 'ГруппаТовара']],
    on='Артикул',
    how='left'
)

# Проверяем, сколько не соединилось
neopred = df['ГруппаТовара'].isna().sum()
print(f'\nНе соединилось: {neopred} из {len(df)} ({neopred/len(df)*100:.1f}%)')

# Заполняем пропуски
df['ГруппаТовара'] = df['ГруппаТовара'].fillna('Без группы')
df['Родитель'] = df['Родитель'].fillna('Без группы')

print('\nГруппы в Модели_v2:')
print(df['ГруппаТовара'].value_counts())

print('\nПо группам и зонам:')
print(df.groupby(['ГруппаТовара', 'Зона']).size().unstack(fill_value=0))

df.to_excel(os.path.join(PROCESSED, '_Расчёт_v2_gruppy.xlsx'), index=False)
print('\nСохранено: _Расчёт_v2_gruppy.xlsx')