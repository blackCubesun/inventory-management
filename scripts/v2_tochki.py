import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем базу
df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_base.xlsx'))
df['Код'] = df['Код'].astype(str).str.zfill(8)

# Загружаем точки заказа
tochki = pd.read_excel(os.path.join(PROCESSED, 'ТочкиЗаказа.xlsx'))
tochki['Код'] = tochki['Код'].astype(str).str.replace("'", "").str.zfill(8)

print('Точки заказа:', tochki.shape)
print('Столбцы:', list(tochki.columns))

# Соединяем по Код + ТипСТО
df = df.merge(
    tochki[['Код', 'ТипСТО', 'Средний', 'P75', 'P90', 'P95', 
            'ТочкаЗаказа_ЦС', 'ТочкаЗаказа_СТО', 'ТочкаЗаказа_ЦС_P90']],
    on=['Код', 'ТипСТО'],
    how='left',
    suffixes=('', '_tochka')
)

# Заполняем пропуски
for col in ['Средний', 'P75', 'P90', 'P95', 'ТочкаЗаказа_ЦС', 'ТочкаЗаказа_СТО', 'ТочкаЗаказа_ЦС_P90']:
    df[col] = df[col].fillna(0)

print(f'\nПосле соединения: {df.shape}')

# Проверяем, сколько позиций получили точки заказа
est_tochki = (df['ТочкаЗаказа_СТО'] > 0).sum()
print(f'Позиций с точками заказа: {est_tochki} из {len(df)}')

print(df[['Код', 'ТипСТО', 'Средний', 'P90', 'ТочкаЗаказа_СТО', 'ТочкаЗаказа_ЦС']].head(20))

df.to_excel(os.path.join(PROCESSED, '_Расчёт_v2_tochki.xlsx'), index=False)
print('\nСохранено: _Расчёт_v2_tochki.xlsx')