import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_gruppy.xlsx'))
df['Артикул'] = df['Артикул'].astype(str).str.strip()
df['Код'] = df['Код'].astype(str).str.zfill(8)

# Без группы
bez = df[df['ГруппаТовара'] == 'Без группы']
print(f'Всего: {len(bez)}')
print(f'\nАртикул пустой: {bez["Артикул"].isna().sum()}')
print(f'Артикул "nan": {(bez["Артикул"] == "nan").sum()}')
print(f'Артикул пустая строка: {(bez["Артикул"] == "").sum()}')

print('\nПримеры:')
print(bez[['СТО', 'Код', 'Артикул', 'Наименование']].head(20))