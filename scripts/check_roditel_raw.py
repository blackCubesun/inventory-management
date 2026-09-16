import pandas as pd
import os

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'

df = pd.read_excel(os.path.join(RAW, 'Родитель.xlsx'), header=None, nrows=30)
print(df.to_string())