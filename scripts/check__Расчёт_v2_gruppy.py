import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'
df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_gruppy.xlsx'))

# Смотрим столбцы
print('Столбцы:')
for i, c in enumerate(df.columns, 1):
    print(f'{i}. {c}')