import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'
V2_PATH = os.path.join(PROCESSED, 'Модель_v2.xlsx')

# Загружаем финальный Расчёт
df_raschet = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_final.xlsx'))
df_raschet['Код'] = df_raschet['Код'].astype(str).str.zfill(8)

# Загружаем Перераспределение
df_pereras = pd.read_excel(os.path.join(PROCESSED, 'Перераспределение_v2.xlsx'))
df_pereras['Код'] = df_pereras['Код'].astype(str).str.zfill(8)

# Загружаем ключи
df_keys = pd.read_excel(os.path.join(PROCESSED, '_Ключи_v3.xlsx'))
df_keys['Код'] = df_keys['Код'].astype(str).str.zfill(8)

# Параметры
params = pd.DataFrame({
    'Параметр': ['МинЗапасДней', 'ЦельЗапасДней', 'LeadTimeЦС', 'LeadTimeСТО', 'Z_95'],
    'Значение': [20, 40, 14, 1, 1.65]
})

# Сохраняем всё
with pd.ExcelWriter(V2_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df_raschet.to_excel(writer, sheet_name='Расчёт', index=False)
    df_pereras.to_excel(writer, sheet_name='Перераспределение', index=False)
    df_keys.to_excel(writer, sheet_name='Ключи', index=False)
    params.to_excel(writer, sheet_name='Параметры', index=False)

print(f'Сохранено в {V2_PATH}')
print(f'  Расчёт: {df_raschet.shape}')
print(f'  Перераспределение: {df_pereras.shape}')
print(f'  Ключи: {df_keys.shape}')
print(f'  Параметры: {params.shape}')