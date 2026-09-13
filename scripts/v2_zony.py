import pandas as pd
import os
import numpy as np

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_tochki.xlsx'))
df['Код'] = df['Код'].astype(str).str.zfill(8)

# Новая логика зон по точкам заказа
def get_zona(row):
    # Нет расхода — неликвид или без движения
    if row['Расход12мес'] == 0:
        if row['ОстатокСТО'] > 0:
            return 'Неликвид'
        else:
            return 'Без движения'
    
    # Есть расход — смотрим на точку заказа
    if row['ДоступныйОстаток'] < row['ТочкаЗаказа_СТО']:
        return 'Крит'
    elif row['ДоступныйОстаток'] > row['ТочкаЗаказа_ЦС'] and row['ТочкаЗаказа_ЦС'] > 0:
        return 'Избыток'
    else:
        return 'Норма'

df['Зона'] = df.apply(get_zona, axis=1)

# Если точки заказа нет — используем старую логику (40 дней)
mask_no_tochka = (df['ТочкаЗаказа_СТО'] == 0) & (df['СДР'] > 0)
df.loc[mask_no_tochka, 'ТочкаЗаказа_СТО'] = df.loc[mask_no_tochka, 'СДР'] * 40
df.loc[mask_no_tochka, 'ТочкаЗаказа_ЦС'] = df.loc[mask_no_tochka, 'СДР'] * 59

# Излишек сверх цели
df['ИзлишекСверхЦели'] = (df['ДоступныйОстаток'] - df['ТочкаЗаказа_ЦС']).clip(lower=0)

# Дефицит до цели
df['ДефицитДоЦели'] = (df['ТочкаЗаказа_СТО'] - df['ДоступныйОстаток']).clip(lower=0)

print('Распределение по зонам:')
print(df['Зона'].value_counts())

df['Код'] = df['Код'].astype(str).str.zfill(8)
df.to_excel(os.path.join(PROCESSED, '_Расчёт_v2_zony.xlsx'), index=False)
print('\nСохранено: _Расчёт_v2_zony.xlsx')