import pandas as pd
import os

RAW = r'C:\Users\92585\Desktop\Sklad_System\data\raw'
PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(RAW, 'Оборотка_3года.xlsx'), skiprows=8, header=0)

# Ключевые столбцы
df = df.rename(columns={
    'Номенклатура.Код': 'Код',
    'Номенклатура.!SKN (Код)': 'SKN',
    'Номенклатура.№ по кат.': 'Артикул',
    'Номенклатура.Наименование': 'Наименование'
})

df = df[df['Код'].notna()]
df = df[~df['Код'].astype(str).str.contains('Итого', na=False)]

# Определяем столбцы СТО — где нет точек, нет Unnamed, нет ключевых
key_cols = ['Код', 'SKN', 'Артикул', 'Наименование']
all_cols = list(df.columns)

# СТО — это столбцы, где нет точек и нет "Unnamed"
sto_indices = []
for i, c in enumerate(all_cols):
    if c in key_cols:
        continue
    if 'Unnamed' in str(c):
        continue
    if '.' in str(c):
        continue
    if c == 'Итого':
        continue
    sto_indices.append(i)

print('Найдено СТО:', len(sto_indices))
for i in sto_indices[:5]:
    print(f'  Индекс {i}: {all_cols[i]}')

# Для каждой СТО — все месяцы до следующей СТО
rows = []
for idx, sto_i in enumerate(sto_indices):
    sto_name = all_cols[sto_i]
    # Конец блока
    if idx + 1 < len(sto_indices):
        sto_end = sto_indices[idx + 1]
    else:
        sto_end = len(all_cols) - 1  # без "Итого"
    
    month_cols = all_cols[sto_i + 1:sto_end]
    
    for month_col in month_cols:
        tmp = df[['Код', 'SKN', 'Артикул', 'Наименование', month_col]].copy()
        tmp.columns = ['Код', 'SKN', 'Артикул', 'Наименование', 'Расход']
        tmp['СТО'] = sto_name
        # Очищаем название месяца от .1, .2
        month_clean = str(month_col).split('.')[0]
        tmp['Месяц'] = month_clean
        rows.append(tmp)

df_flat = pd.concat(rows, ignore_index=True)
df_flat = df_flat[df_flat['Расход'].notna()]
df_flat['Расход'] = pd.to_numeric(df_flat['Расход'], errors='coerce')
df_flat = df_flat[df_flat['Расход'] > 0]

print(f'\nСтрок в результате: {len(df_flat)}')
print(df_flat.head(10))

df_flat.to_excel(os.path.join(PROCESSED, 'Оборотка_3года_плоский.xlsx'), index=False)
print('\nСохранено: Оборотка_3года_плоский.xlsx')