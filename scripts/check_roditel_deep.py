import pandas as pd
import os

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'

df = pd.read_excel(os.path.join(RAW, 'Родитель.xlsx'), skiprows=7, header=0, nrows=20)
print('Размер:', df.shape)
print('Колонки:', list(df.columns))
print('n\Первые 20 строк:')
print(df.head(20))