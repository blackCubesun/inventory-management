import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_full.xlsx'))
df['Код'] = df['Код'].astype(str).str.zfill(8)

# НужноПереместить с ЦС
df['НужноПереместитьЦС'] = df.apply(
    lambda r: min(
        max(0, r['ТочкаЗаказа_СТО'] - r['ДоступныйОстаток']),
        r['СвободноЦС']
    ) if r['Зона'] == 'Крит' else 0,
    axis=1
)

# НужноЗаказать — только если нет на ЦС и нет у других СТО
df['НужноЗаказать'] = df.apply(
    lambda r: max(0, r['ТочкаЗаказа_ЦС'] - r['ОстатокЦС']) 
    if r['Зона'] == 'Крит' and r['СвободноЦС'] == 0 else 0,
    axis=1
)

# Излишек
df['ИзлишекКПеремещению'] = df.apply(
    lambda r: r['ИзлишекСверхЦели'] if r['Зона'] == 'Избыток' else 0,
    axis=1
)

# Сводка
summary = df.groupby('Зона').agg({
    'Код': 'count',
    'ОстатокСТО': 'sum',
    'НужноПереместитьЦС': 'sum',
    'НужноЗаказать': 'sum',
    'ИзлишекКПеремещению': 'sum'
}).round(0)
summary.columns = ['Позиций', 'ОстатокШт', 'ПереместитьЦС_Шт', 'Заказать_Шт', 'Излишек_Шт']

print('Сводка по зонам:')
print(summary)

# Принудительно текст
df['Код'] = df['Код'].astype(str)
df.to_excel(os.path.join(PROCESSED, '_Расчёт_v2_final.xlsx'), index=False)
print('\nСохранено: _Расчёт_v2_final.xlsx')