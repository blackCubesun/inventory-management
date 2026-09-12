import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df_probeg = pd.read_excel(os.path.join(PROCESSED, 'Пробег_динамика.xlsx'))
df_models = pd.read_excel(os.path.join(PROCESSED, 'Справочник_Модели.xlsx'))

print(df_models)
print('\nДинамика:')
print(df_probeg.head())