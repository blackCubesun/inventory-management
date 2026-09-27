import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_gruppy.xlsx'))
df['Код'] = df['Код'].astype(str).str.zfill(8)

# Общий расход по Коду
obshiy = df.groupby('Код')['Расход12мес'].sum().reset_index()
obshiy.columns = ['Код', 'ОбщийРасходПоКомпании']

df = df.merge(obshiy, on='Код', how='left')

# Признак: локальный неликвид, но глобальный ликвид
df['Востребован'] = (
    (df['Расход12мес'] == 0) & 
    (df['ОбщийРасходПоКомпании'] >= 1)
).astype(int)

# Глобальный неликвид (не нужен нигде)
df['ГлобальныйНеликвид'] = (
    (df['Расход12мес'] == 0) & 
    (df['ОбщийРасходПоКомпании'] == 0) &
    (df['ОстатокСТО'] > 0)
).astype(int)

print('Распределение:')
print(f'Локальный неликвид: {(df["Расход12мес"] == 0).sum()}')
print(f'Востребован: {df["Востребован"].sum()}')
print(f'Глобальный неликвид: {df["ГлобальныйНеликвид"].sum()}')

print('\nПо СТО (топ-10):')
print(df[df['Востребован'] == 1].groupby('СТО').size().sort_values(ascending=False).head(10))

df.to_excel(os.path.join(PROCESSED, '_Расчёт_v2_vostrebovan.xlsx'), index=False)
print('\nСохранено: _Расчёт_v2_vostrebovan.xlsx')