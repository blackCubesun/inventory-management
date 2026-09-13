import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_tochki.xlsx'))

# Всего позиций
total = len(df)
print(f'Всего строк (СТО+Код): {total}')

# Ликвид на СТО
likvid_sto = (df['Расход12мес'] > 0).sum()
print(f'Ликвид на СТО (расход > 0): {likvid_sto} ({likvid_sto/total*100:.1f}%)')

# Ликвид по компании — считаем уникальные Коды с расходом
kody_s_rashodom = df[df['Расход12мес'] > 0]['Код'].unique()
print(f'Уникальных ликвидных Кодов: {len(kody_s_rashodom)}')

# Сколько строк имеют Код, который ликвиден где-то в компании
df['ЛиквидКомпания'] = df['Код'].isin(kody_s_rashodom)
likvid_comp = df['ЛиквидКомпания'].sum()
print(f'Строк с Кодом, ликвидным где-то: {likvid_comp} ({likvid_comp/total*100:.1f}%)')

# Неликвид локальный, но ликвид глобальный
nelikvid_sto_likvid_comp = df[
    (df['Расход12мес'] == 0) & (df['ЛиквидКомпания'])
]
print(f'\nНеликвид на СТО, но ликвид в компании: {len(nelikvid_sto_likvid_comp)}')
print(nelikvid_sto_likvid_comp[['СТО', 'Код', 'Наименование', 'ОстатокСТО']].head(20))