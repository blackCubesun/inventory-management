import pandas as pd
import os
import re

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_final.xlsx'))
df['Код'] = df['Код'].astype(str).str.zfill(8)

# Список маркеров расходных материалов
rashodnye_markers = [
    'скоба', 'клипса', 'стяжка', 'саморез',
    'изолента', 'скотч', 'ветошь', 'салфетка'
]

def is_rashodny(row):
    name = str(row['Наименование']).lower()
    for marker in rashodnye_markers:
        if marker in name:
            return 'Да'
    return 'Нет'

df['РасходныйМатериал'] = df.apply(is_rashodny, axis=1)

print('Распределение:')
print(df['РасходныйМатериал'].value_counts())

print('\nПримеры расходных:')
rash = df[df['РасходныйМатериал'] == 'Да']
print(rash['Наименование'].head(30).tolist())

print('\nПримеры запчастей:')
zap = df[df['РасходныйМатериал'] == 'Нет']
print(zap['Наименование'].head(30).tolist())

df.to_excel(os.path.join(PROCESSED, '_Расчёт_v2_classified.xlsx'), index=False)
print('\nСохранено: _Расчёт_v2_classified.xlsx')