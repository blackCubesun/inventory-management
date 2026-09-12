import pandas as pd
import os
from openpyxl import load_workbook

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'
MODEL_PATH = os.path.join(PROCESSED, 'Модель.xlsx')

# Загружаем справочник
df_sto = pd.read_excel(os.path.join(PROCESSED, 'Справочник_СТО.xlsx'))
print('Справочник:')
print(df_sto)

# Открываем Модель
with pd.ExcelWriter(MODEL_PATH, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df_sto.to_excel(writer, sheet_name='_СТО', index=False)

print('\nЛист _СТО добавлен в Модель.xlsx')

# Скрываем лист
wb = load_workbook(MODEL_PATH)
ws = wb['_СТО']
ws.sheet_state = 'hidden'
wb.save(MODEL_PATH)
print('Лист _СТО скрыт')