import pandas as pd
import os

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'
PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(RAW, 'Родитель.xlsx'), header=None, skiprows=9)

df = df[[0, 3, 4]]
df.columns = ['Номенклатура', 'Родитель', 'Артикул']

df = df[df['Артикул'].notna()]
df = df[df['Родитель'].notna()]

# Убираем строку с заголовками
df = df[df['Артикул'] != '№ по кат.']

df = df.drop_duplicates(subset=['Артикул'])

print(f'Товаров: {len(df)}')
print(df.head(20))

df.to_excel(os.path.join(PROCESSED, 'Иерархия_товаров.xlsx'), index=False)
print('\nСохранено: Иерархия_товаров.xlsx')
print(df['Родитель'].value_counts())