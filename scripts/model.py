import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем все плоские файлы
df_ostatki = pd.read_excel(os.path.join(PROCESSED, 'Остатки_плоский.xlsx'))
df_vputi = pd.read_excel(os.path.join(PROCESSED, 'ВПути_плоский.xlsx'))
df_rezerv = pd.read_excel(os.path.join(PROCESSED, 'Резервы_плоский.xlsx'))
df_mes = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_месяц_плоский.xlsx'))
df_god = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_год_плоский.xlsx'))
df_cena = pd.read_excel(os.path.join(PROCESSED, 'Цена_плоский.xlsx'))

# Приводим Код к строке
for df in [df_ostatki, df_vputi, df_rezerv, df_mes, df_god, df_cena]:
    df['Код'] = df['Код'].astype(str).str.strip()

print('Остатки:', df_ostatki.shape)
print('ВПути:', df_vputi.shape)
print('Резервы:', df_rezerv.shape)
print('Месяц:', df_mes.shape)
print('Год:', df_god.shape)
print('Цена:', df_cena.shape)

# Собираем все пары СТО+Код из всех файлов
keys_list = []

for df in [df_ostatki, df_vputi, df_rezerv, df_mes, df_god]:
    tmp = df[['Код', 'СТО']].copy()
    keys_list.append(tmp)

# Приводим Код к строке с ведущими нулями (8 знаков)
for df in [df_ostatki, df_vputi, df_rezerv, df_mes, df_god, df_cena]:
    df['Код'] = df['Код'].astype(str).str.strip()
    df['Код'] = df['Код'].str.zfill(8)

# Собираем все пары СТО+Код
keys_list = []

for df in [df_ostatki, df_vputi, df_rezerv, df_mes, df_god]:
    tmp = df[['Код', 'СТО']].copy()
    keys_list.append(tmp)

df_keys = pd.concat(keys_list, ignore_index=True)
df_keys = df_keys.drop_duplicates()

# Добавляем SKN, Артикул, Наименование из Года
df_info = df_god[['Код', 'SKN', 'Артикул', 'Наименование']].drop_duplicates(subset=['Код'])
df_keys = df_keys.merge(df_info, on='Код', how='left')

print('Ключей:', df_keys.shape)
print(df_keys.head(10))

# Годовой расход по Коду+СТО (без SKN)
df_god_agg = df_god.groupby(['Код', 'СТО'])['Расход'].sum().reset_index()
df_god_agg.columns = ['Код', 'СТО', 'Расход12мес']

# Годовой расход по Коду+SKN (аналоги)
df_god_skn = df_god.groupby(['SKN', 'СТО'])['Расход'].sum().reset_index()
df_god_skn.columns = ['SKN', 'СТО', 'Расход12мес_SKN']

# Присоединяем к ключам
df = df_keys.merge(df_god_agg, on=['Код', 'СТО'], how='left')
df['Расход12мес'] = df['Расход12мес'].fillna(0)

# Убираем мусор
df = df[df['Код'].notna()]
df = df[df['Код'] != 'Итого']
df = df[~df['Код'].str.contains('Итого', na=False)]

# СДР
df['СДР'] = df['Расход12мес'] / 365

print(df[['Код', 'СТО', 'Расход12мес', 'СДР']].head(10))
print('\nСтрок с расходом > 0:', (df['Расход12мес'] > 0).sum())

# Остатки СТО (по Коду, без SKN)
df_ost_agg = df_ostatki.groupby(['Код', 'СТО'])['Остаток'].sum().reset_index()
df_ost_agg.columns = ['Код', 'СТО', 'ОстатокСТО']
df = df.merge(df_ost_agg, on=['Код', 'СТО'], how='left')
df['ОстатокСТО'] = df['ОстатокСТО'].fillna(0)

# Остаток по SKN (сумма аналогов)
df_ost_skn = df_ostatki.groupby(['SKN', 'СТО'])['Остаток'].sum().reset_index()
df_ost_skn.columns = ['SKN', 'СТО', 'ОстатокСТО_SKN']

df = df.merge(df_ost_skn, on=['SKN', 'СТО'], how='left')
df['ОстатокСТО_SKN'] = df['ОстатокСТО_SKN'].fillna(df['ОстатокСТО'])

# ВПути
df_vp_agg = df_vputi.groupby(['Код', 'СТО'])['ВПути'].sum().reset_index()
df = df.merge(df_vp_agg, on=['Код', 'СТО'], how='left')
df['ВПути'] = df['ВПути'].fillna(0)

# Оборот за месяц
df_mes_agg = df_mes.groupby(['Код', 'СТО'])['РасходМес'].sum().reset_index()
df_mes_agg.columns = ['Код', 'СТО', 'ОборотМес']
df = df.merge(df_mes_agg, on=['Код', 'СТО'], how='left')
df['ОборотМес'] = df['ОборотМес'].fillna(0)

# Резервы
df_rez_agg = df_rezerv.groupby(['Код', 'СТО'])['Резерв'].sum().reset_index()
df = df.merge(df_rez_agg, on=['Код', 'СТО'], how='left')
df['Резерв'] = df['Резерв'].fillna(0)

# Доступный остаток
df['ДоступныйОстаток'] = df['ОстатокСТО'] + df['ВПути']

# Дней хватит
df['ДнейХватит'] = df.apply(lambda x: x['ДоступныйОстаток'] / x['СДР'] if x['СДР'] > 0 else 0, axis=1)

print(df[['Код', 'СТО', 'ОстатокСТО', 'ВПути', 'ОборотМес', 'Резерв', 'ДоступныйОстаток', 'ДнейХватит']].head(10))

# Зона
def get_zona(row):
    if row['Расход12мес'] == 0 and row['ОстатокСТО'] > 0:
        return 'Неликвид'
    elif row['СДР'] == 0:
        return 'Без движения'
    elif row['ДнейХватит'] < 20:
        return 'Крит'
    elif row['ДнейХватит'] <= 40:
        return 'Норма'
    else:
        return 'Избыток'

df['Зона'] = df.apply(get_zona, axis=1)

# Излишек неликвид
df['ИзлишекНеликвид'] = df.apply(lambda x: x['ОстатокСТО'] if x['Расход12мес'] == 0 and x['ОстатокСТО'] > 0 else 0, axis=1)

# Остаток ЦС (по Коду, все СТО)
df_cs = df_ostatki[df_ostatki['СТО'] == 'Подразделение Склад оптовый ОТХ (Сокол)'].groupby('Код')['Остаток'].sum().reset_index()
df_cs.columns = ['Код', 'ОстатокЦС']
df = df.merge(df_cs, on='Код', how='left')
df['ОстатокЦС'] = df['ОстатокЦС'].fillna(0)

# Резерв по Коду (все СТО)
df_rez_all = df_rezerv.groupby('Код')['Резерв'].sum().reset_index()
df_rez_all.columns = ['Код', 'РезервЦС']
df = df.merge(df_rez_all, on='Код', how='left')
df['РезервЦС'] = df['РезервЦС'].fillna(0)

# Свободно на ЦС
df['СвободноЦС'] = df['ОстатокЦС'] - df['РезервЦС']
df['СвободноЦС'] = df['СвободноЦС'].clip(lower=0)

# Целевой запас
df['ЦелевойЗапасШт'] = df['СДР'] * 40

# Дефицит
df['ДефицитДоЦели'] = (df['ЦелевойЗапасШт'] - df['ДоступныйОстаток']).clip(lower=0)

# Излишек сверх цели
df['ИзлишекСверхЦели'] = df.apply(lambda x: x['ДоступныйОстаток'] - x['ЦелевойЗапасШт'] if x['ДнейХватит'] > 40 else 0, axis=1)

# Нужно переместить
def need_move(row):
    if row['ДнейХватит'] >= 20 or row['Зона'] in ['Неликвид', 'Без движения']:
        return 0
    return min(
        max(0, row['СДР'] * 40 - row['ДоступныйОстаток']),
        row['СДР'] * 30,
        row['СвободноЦС']
    )

df['НужноПереместить'] = df.apply(need_move, axis=1)

print(df[['Код', 'СТО', 'Зона', 'ОстатокЦС', 'РезервЦС', 'СвободноЦС', 'НужноПереместить']].head(15))
print('\nРаспределение по зонам:')
print(df['Зона'].value_counts())

# ===== ABC =====
# Стоимость расхода
df = df.merge(df_cena[['Код', 'Цена']], on='Код', how='left')
df['СтоимостьРасхода'] = df['Расход12мес'] * df['Цена'].fillna(0)

# ABC по коду (не по СТО)
abc = df.groupby('Код')['СтоимостьРасхода'].sum().reset_index()
abc = abc.sort_values('СтоимостьРасхода', ascending=False)
abc['НакопПроцент'] = abc['СтоимостьРасхода'].cumsum() / abc['СтоимостьРасхода'].sum()
abc['ABC'] = abc['НакопПроцент'].apply(lambda x: 'A' if x <= 0.8 else ('B' if x <= 0.95 else 'C'))
df = df.merge(abc[['Код', 'ABC']], on='Код', how='left')

# ===== XYZ =====
# Сколько месяцев с расходом
xyz = df_god.groupby(['Код', 'СТО'])['Месяц'].nunique().reset_index()
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

# ABC+XYZ
df['ABC_XYZ'] = df['ABC'] + df['XYZ']

print(df[['Код', 'СТО', 'ABC', 'XYZ', 'ABC_XYZ', 'СтоимостьРасхода']].head(10))
print('\nABC распределение:')
print(df['ABC'].value_counts())
print('\nXYZ распределение:')
print(df['XYZ'].value_counts())

# Сохраняем результат
df.to_excel('Модель.xlsx', index=False)
print('\nСохранено: Модель.xlsx')
print('Итоговые столбцы:', list(df.columns))

print('\nПроверка ОстатокСТО_SKN:')
print(df[['Код', 'СТО', 'ОстатокСТО', 'ОстатокСТО_SKN']].head(10))

df.to_excel(os.path.join(PROCESSED, 'Модель.xlsx'), index=False)
print('\nСохранено: Модель.xlsx')
