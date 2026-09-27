import pandas as pd
import os
import math

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_vostrebovan.xlsx'))
df['Код'] = df['Код'].astype(str).str.zfill(8)

# Отправители: неликвид + остаток
otpravitel = df[(df['Зона'] == 'Неликвид') & (df['ОстатокСТО'] > 0)][[
    'СТО', 'Код', 'SKN', 'Артикул', 'Наименование', 'ТипСТО',
    'ОстатокСТО', 'ОстатокЦС', 'СвободноЦС'
]].copy()
otpravitel.columns = [
    'Откуда', 'Код', 'SKN', 'Артикул', 'Наименование', 'ТипСТО_Откуда',
    'ОстатокНаСТО', 'ОстатокЦС', 'СвободноЦС'
]

# Получатели: расход >= 1
poluchatel = df[df['Расход12мес'] >= 1][[
    'СТО', 'Код', 'ТипСТО', 'Расход12мес', 'ДоступныйОстаток', 'ТочкаЗаказа_СТО'
]].copy()
poluchatel.columns = [
    'Куда', 'Код', 'ТипСТО_Куда', 'РасходТам', 'ОстатокТам', 'ТочкаЗаказаТам'
]

poluchatel['Дефицит'] = (poluchatel['ТочкаЗаказаТам'] - poluchatel['ОстатокТам']).clip(lower=0)
poluchatel = poluchatel[poluchatel['Дефицит'] >= 1]

# Соединяем
result = otpravitel.merge(poluchatel, on='Код', how='inner')
result = result[result['Откуда'] != result['Куда']]

# Сортируем: Дефицит (убыв), РасходТам (убыв), ОстатокТам (возр)
result = result.sort_values(
    ['Код', 'Дефицит', 'РасходТам', 'ОстатокТам'],
    ascending=[True, False, False, True]
)

# Объём
result['СколькоПереместить'] = result[['ОстатокНаСТО', 'Дефицит']].min(axis=1)
result['СколькоПереместить'] = result['СколькоПереместить'].apply(math.ceil)
result = result[result['СколькоПереместить'] >= 1]

# ===== ДЛЯ АДМИНА: все пары =====
admin = result.copy()
admin.to_excel(os.path.join(PROCESSED, 'Перераспределение_админ.xlsx'), index=False)
print(f'Админ: {len(admin)} строк')

# ===== ДЛЯ КЛАДОВЩИКА: ТОП-3 получателя =====
# Оставляем первые 3 для каждой пары (Откуда, Код)
kladovshik = result.groupby(['Откуда', 'Код']).head(3).copy()

# Добавляем ранг
kladovshik['Ранг'] = kladovshik.groupby(['Откуда', 'Код']).cumcount() + 1

kladovshik.to_excel(os.path.join(PROCESSED, 'Перераспределение_кладовщик.xlsx'), index=False)
print(f'Кладовщик: {len(kladovshik)} строк')

# Проверяем: сколько пар имеют 3 варианта
pairs_count = kladovshik.groupby(['Откуда', 'Код']).size().value_counts()
print(f'\nРаспределение пар по количеству вариантов:')
print(pairs_count)

print('\nПример (первые 10):')
print(kladovshik[['Откуда', 'Код', 'Наименование', 'Куда', 'РасходТам', 'ОстатокТам', 'Дефицит', 'СколькоПереместить', 'Ранг']].head(10))