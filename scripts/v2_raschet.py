import pandas as pd
import os
import numpy as np

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем ключи
df = pd.read_excel(os.path.join(PROCESSED, '_Ключи_v3.xlsx'))
df['Код'] = df['Код'].astype(str).str.zfill(8)

# Загружаем вспомогательные
df_sto = pd.read_excel(os.path.join(PROCESSED, 'Справочник_СТО.xlsx'))
df_tochki = pd.read_excel(os.path.join(PROCESSED, 'ТочкиЗаказа.xlsx'))
df_tochki['Код'] = df_tochki['Код'].astype(str).str.zfill(8)

# Загружаем плоские
df_ost = pd.read_excel(os.path.join(PROCESSED, 'Остатки_плоский.xlsx'))
df_ost['Код'] = df_ost['Код'].astype(str).str.zfill(8)

df_rashod = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_год_плоский.xlsx'))
df_rashod['Код'] = df_rashod['Код'].astype(str).str.zfill(8)

df_vp = pd.read_excel(os.path.join(PROCESSED, 'ВПути_плоский.xlsx'))
df_vp['Код'] = df_vp['Код'].astype(str).str.zfill(8)

df_rez = pd.read_excel(os.path.join(PROCESSED, 'Резервы_плоский_испр.xlsx'))
df_rez['Код'] = df_rez['Код'].astype(str).str.zfill(8)

df_mes = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_месяц_плоский.xlsx'))
df_mes['Код'] = df_mes['Код'].astype(str).str.zfill(8)

print('Данные загружены')

# ===== ТипСТО =====
df = df.merge(df_sto, on='СТО', how='left')

# ===== Расход12мес =====
rashod_agg = df_rashod.groupby(['Код', 'СТО'])['Расход'].sum().reset_index()
rashod_agg.columns = ['Код', 'СТО', 'Расход12мес']
df = df.merge(rashod_agg, on=['Код', 'СТО'], how='left')
df['Расход12мес'] = df['Расход12мес'].fillna(0)

# ===== СДР =====
df['СДР'] = df['Расход12мес'] / 365

# ===== ОстатокСТО =====
ost_agg = df_ost.groupby(['Код', 'СТО'])['Остаток'].sum().reset_index()
ost_agg.columns = ['Код', 'СТО', 'ОстатокСТО']
df = df.merge(ost_agg, on=['Код', 'СТО'], how='left')
df['ОстатокСТО'] = df['ОстатокСТО'].fillna(0)

# ===== ВПути =====
vp_agg = df_vp.groupby(['Код', 'СТО'])['ВПути'].sum().reset_index()
df = df.merge(vp_agg, on=['Код', 'СТО'], how='left')
df['ВПути'] = df['ВПути'].fillna(0)

# ===== ОборотМес =====
mes_agg = df_mes.groupby(['Код', 'СТО'])['РасходМес'].sum().reset_index()
mes_agg.columns = ['Код', 'СТО', 'ОборотМес']
df = df.merge(mes_agg, on=['Код', 'СТО'], how='left')
df['ОборотМес'] = df['ОборотМес'].fillna(0)

# ===== ДоступныйОстаток =====
df['ДоступныйОстаток'] = df['ОстатокСТО'] + df['ВПути']

# ===== ДнейХватит =====
df['ДнейХватит'] = df.apply(
    lambda r: r['ДоступныйОстаток'] / r['СДР'] if r['СДР'] > 0 else 0,
    axis=1
)

# ===== ОстатокЦС =====
cs = df_ost[df_ost['СТО'] == 'Подразделение Склад оптовый ОТХ (Сокол)']
cs_agg = cs.groupby('Код')['Остаток'].sum().reset_index()
cs_agg.columns = ['Код', 'ОстатокЦС']
df = df.merge(cs_agg, on='Код', how='left')
df['ОстатокЦС'] = df['ОстатокЦС'].fillna(0)

# ===== РезервЦС =====
rez_agg = df_rez.groupby('Код')['Резерв'].sum().reset_index()
rez_agg.columns = ['Код', 'РезервЦС']
df = df.merge(rez_agg, on='Код', how='left')
df['РезервЦС'] = df['РезервЦС'].fillna(0)

# ===== СвободноЦС =====
df['СвободноЦС'] = (df['ОстатокЦС'] - df['РезервЦС']).clip(lower=0)

print(f'Расчёт собран: {df.shape}')
print(df.head())

df['Код'] = df['Код'].astype(str).str.zfill(8)
df.to_excel(os.path.join(PROCESSED, '_Расчёт_v2_base.xlsx'), index=False)
print('\nСохранено: _Расчёт_v2_base.xlsx')