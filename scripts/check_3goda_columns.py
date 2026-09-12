import pandas as pd
import os

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'

df = pd.read_excel(os.path.join(RAW, 'Оборотка_3года.xlsx'), skiprows=8, header=0, nrows=0)

cols = list(df.columns)
print('Всего колонок:', len(cols))
print('\nПервые 50:')
for i, c in enumerate(cols[:50]):
    print(f'{i}: {c}')