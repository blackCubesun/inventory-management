import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'
V2_PATH = os.path.join(PROCESSED, 'Модель_v2.xlsx')

df = pd.read_excel(V2_PATH, sheet_name='Расчёт')
df['Код'] = df['Код'].astype(str).str.zfill(8)

print('Столбцы:')
for i, c in enumerate(df.columns, 1):
    print(f'{i}. {c}')

print('\n=== Сводка по зонам ===')
summary = df.groupby('Зона').agg({
    'Код': 'count',
    'ОстатокСТО': 'sum',
    'НужноПереместитьЦС': 'sum',
    'НужноЗаказать': 'sum',
    'ИзлишекКПеремещению': 'sum'
}).round(0)
summary.columns = ['Позиций', 'ОстатокШт', 'ПереместитьЦС', 'Заказать', 'Излишек']
print(summary)

print('\n=== ABC_XYZ ===')
print(df['ABC_XYZ'].value_counts().head(10))