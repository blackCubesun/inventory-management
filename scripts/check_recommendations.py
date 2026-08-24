import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'
df = pd.read_excel(os.path.join(PROCESSED, 'Модель.xlsx'))

sto_name = 'Подразделение 10А (Марьина Роща)'  # замени на свою
df_sto = df[df['СТО'] == sto_name]

# Сколько в Крите
krit = df_sto[df_sto['Зона'] == 'Крит']
print(f'Позиций в Крите: {len(krit)}')

# У скольких есть свободно на ЦС
print(f'Из них со свободным ЦС: {(krit["СвободноЦС"] > 0).sum()}')

# Пример одной позиции
print('\nПример позиции в Крите:')
print(krit[['Код', 'SKN', 'Наименование', 'ОстатокСТО', 'ОстатокЦС', 'РезервЦС', 'СвободноЦС', 'СДР', 'ДнейХватит', 'НужноПереместить']].head(10))