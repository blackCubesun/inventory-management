import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'
NEW_MODEL = os.path.join(PROCESSED, 'Модель_v2.xlsx')

# Создаём файл с пустым листом
with pd.ExcelWriter(NEW_MODEL, engine='openpyxl') as writer:
    pd.DataFrame().to_excel(writer, sheet_name='Расчёт', index=False)

print(f'Создан: {NEW_MODEL}')