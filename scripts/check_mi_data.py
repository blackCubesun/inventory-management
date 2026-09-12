import pandas as pd
import os

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'

files = ['Оборотка_3года.xlsx', 'Пробег.xlsx', 'Погода.xlsx']

for f in files:
    try:
        df = pd.read_excel(os.path.join(RAW, f), nrows=5)
        print(f'\n=== {f} ===')
        print(f'Размер: {df.shape}')
        print(f'Столбцы: {list(df.columns)}')
        print(df.head())
    except Exception as e:
        print(f'\n✗ {f}: {e}')