import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df_base = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_base.xlsx'))
df_tochki = pd.read_excel(os.path.join(PROCESSED, 'ТочкиЗаказа.xlsx'))

print('Код в базе:', df_base['Код'].head(5).tolist())
print('Код в точках:', df_tochki['Код'].head(5).tolist())

print('\nТипы:')
print('База:', df_base['Код'].dtype)
print('Точки:', df_tochki['Код'].dtype)

# Проверим конкретный код
test_kod = '00000008'
print(f'\nИщем {test_kod}:')
print('В базе:', (df_base['Код'] == test_kod).sum())
print('В точках:', (df_tochki['Код'] == test_kod).sum())