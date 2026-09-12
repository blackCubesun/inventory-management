import pandas as pd
import os

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'

files = ['Оборотка_3года.xlsx', 'Пробег.xlsx', 'Погода.xlsx']

for f in files:
    print(f'\n=== {f} ===')
    df = pd.read_excel(os.path.join(RAW, f), header=None, nrows=20)
    for i in range(min(20, len(df))):
        row = df.iloc[i].tolist()
        # Показываем непустые строки
        if any(pd.notna(x) for x in row):
            print(f'{i}: {row[:6]}')