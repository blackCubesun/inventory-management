import pandas as pd
import os

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'

df = pd.read_excel(os.path.join(RAW, 'Пробег.xlsx'), skiprows=5, header=0)
df = df.dropna(subset=['Автомобиль'])

print('Всего машин:', df['Автомобиль'].nunique())
print('\nВладельцы:')
print(df['Владелец'].value_counts())
print('\nПримеры автомобилей:')
for car in df['Автомобиль'].unique()[:10]:
    print(f'  {car}')