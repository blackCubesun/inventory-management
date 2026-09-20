import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# ML-датасет
df = pd.read_excel(os.path.join(PROCESSED, 'ML_Dataset_v2.xlsx'))
df['Код'] = df['Код'].astype(str).str.zfill(8)

# Иерархия
df_ier = pd.read_excel(os.path.join(PROCESSED, 'Иерархия_товаров_укрупнённая.xlsx'))
df_ier['Артикул'] = df_ier['Артикул'].astype(str)

# В ML-датасете есть Артикул?
print('Колонки ML:', list(df.columns))

if 'Артикул' not in df.columns:
    # Подтягиваем артикул из Расчёта
    df_raschet = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_gruppy.xlsx'))
    df_raschet['Код'] = df_raschet['Код'].astype(str).str.zfill(8)
    
    artikul = df_raschet[['Код', 'Артикул', 'ГруппаТовара']].drop_duplicates(subset=['Код'])
    df = df.merge(artikul, on='Код', how='left')
else:
    df = df.merge(df_ier[['Артикул', 'ГруппаТовара']], on='Артикул', how='left')

df['ГруппаТовара'] = df['ГруппаТовара'].fillna('Без группы')

print('\nГруппы в ML:')
print(df['ГруппаТовара'].value_counts())

df.to_excel(os.path.join(PROCESSED, 'ML_Dataset_v3.xlsx'), index=False)
print('\nСохранено: ML_Dataset_v3.xlsx')