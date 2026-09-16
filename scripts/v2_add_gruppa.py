import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем финальный Расчёт v2
df_model = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_final.xlsx'))
df_model['Артикул'] = df_model['Артикул'].astype(str)

# Загружаем иерархию
df_ier = pd.read_excel(os.path.join(PROCESSED, 'Иерархия_товаров_укрупнённая.xlsx'))
df_ier['Артикул'] = df_ier['Артикул'].astype(str)

# Соединяем
df_model = df_model.merge(
    df_ier[['Артикул', 'ГруппаТовара']],
    on='Артикул',
    how='left'
)

# Заполняем пропуски
df_model['ГруппаТовара'] = df_model['ГруппаТовара'].fillna('Не определено')

print('Группы в модели:')
print(df_model['ГруппаТовара'].value_counts())

print('\nПо группам и зонам:')
print(df_model.groupby(['ГруппаТовара', 'Зона']).size().unstack(fill_value=0))

df_model.to_excel(os.path.join(PROCESSED, '_Расчёт_v2_gruppy.xlsx'), index=False)
print('\nСохранено: _Расчёт_v2_gruppy.xlsx')