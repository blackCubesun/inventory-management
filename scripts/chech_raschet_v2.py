import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_gruppy.xlsx'))
neopred = df[df['ГруппаТовара'] == 'Не определено']
print('Примеры:')
print(neopred[['Код', 'Артикул', 'Наименование']].head(20))
print('\nАртикул пустой:', neopred['Артикул'].isna().sum())
print('Артикул "nan":', (neopred['Артикул'] == 'nan').sum())