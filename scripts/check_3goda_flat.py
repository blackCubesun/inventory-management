import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_3года_плоский.xlsx'))

print('Размер:', df.shape)
print('\nУникальных СТО:', df['СТО'].nunique())
print(df['СТО'].unique())
print('\nУникальных месяцев:', df['Месяц'].nunique())
print(sorted(df['Месяц'].unique()))
print('\nОбщий расход:', df['Расход'].sum())