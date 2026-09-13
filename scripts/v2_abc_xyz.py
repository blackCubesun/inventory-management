import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_zony.xlsx'))
df['Код'] = df['Код'].astype(str).str.zfill(8)

# ===== ABC =====
# Загружаем цены
df_cena = pd.read_excel(os.path.join(PROCESSED, 'Цена_плоский.xlsx'))
df_cena['Код'] = df_cena['Код'].astype(str).str.zfill(8)

# Стоимость расхода по Коду
df = df.merge(df_cena[['Код', 'Цена']], on='Код', how='left')
df['Цена'] = df['Цена'].fillna(0)
df['СтоимостьРасхода'] = df['Расход12мес'] * df['Цена']

# ABC по Коду (сумма по всем СТО)
abc = df.groupby('Код')['СтоимостьРасхода'].sum().reset_index()
abc = abc.sort_values('СтоимостьРасхода', ascending=False)

total = abc['СтоимостьРасхода'].sum()
abc['НакопПроцент'] = abc['СтоимостьРасхода'].cumsum() / total if total > 0 else 0
abc['ABC'] = abc['НакопПроцент'].apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))

df = df.merge(abc[['Код', 'ABC']], on='Код', how='left')

# ===== XYZ =====
# Загружаем помесячный расход
df_god = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_год_плоский.xlsx'))
df_god['Код'] = df_god['Код'].astype(str).str.zfill(8)

# Сколько месяцев был расход
xyz = df_god[df_god['Расход'] > 0].groupby(['Код', 'СТО'])['Месяц'].nunique().reset_index()
xyz.columns = ['Код', 'СТО', 'МесяцевСРасходом']

df = df.merge(xyz, on=['Код', 'СТО'], how='left')
df['МесяцевСРасходом'] = df['МесяцевСРасходом'].fillna(0)

def get_xyz(m):
    if m >= 10:
        return 'X'
    elif m >= 4:
        return 'Y'
    else:
        return 'Z'

df['XYZ'] = df['МесяцевСРасходом'].apply(get_xyz)
df['ABC_XYZ'] = df['ABC'] + df['XYZ']

print('ABC:')
print(df['ABC'].value_counts())
print('\nXYZ:')
print(df['XYZ'].value_counts())
print('\nABC_XYZ (топ-10):')
print(df['ABC_XYZ'].value_counts().head(10))

df['Код'] = df['Код'].astype(str).str.zfill(8)
df.to_excel(os.path.join(PROCESSED, '_Расчёт_v2_full.xlsx'), index=False)
print('\nСохранено: _Расчёт_v2_full.xlsx')