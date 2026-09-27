import pandas as pd
import os

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

# Получатели: расход >= 1, дефицит
poluchatel = df[df['Расход12мес'] >= 1][[
    'СТО', 'Код', 'Расход12мес', 'ДоступныйОстаток', 'ТочкаЗаказа_СТО'
]].copy()
poluchatel.columns = [
    'Куда', 'Код', 'РасходТам', 'ОстатокТам', 'ТочкаЗаказаТам'
]

# Дефицит получателя
poluchatel['Дефицит'] = (poluchatel['ТочкаЗаказаТам'] - poluchatel['ОстатокТам']).clip(lower=0)

# Оставляем только тех, кому реально нужно
poluchatel = poluchatel[poluchatel['Дефицит'] >= 1]

print(f'Отправителей: {len(otpravitel)}')
print(f'Получателей: {len(poluchatel)}')

# Соединяем
result = otpravitel.merge(poluchatel, on='Код', how='inner')

# Убираем СТО → СТО
result = result[result['Откуда'] != result['Куда']]

print(f'Всего пар: {len(result)}')

# Сортируем: по Коду, потом по Дефициту (убывание), потом по Остатку получателя (возрастание)
result = result.sort_values(
    ['Код', 'Дефицит', 'ОстатокТам'],
    ascending=[True, False, True]
)

# Объём к перемещению
result['СколькоПереместить'] = result[['ОстатокНаСТО', 'Дефицит']].min(axis=1)

# Убираем мелочь
result = result[result['СколькоПереместить'] >= 1]

# ===== ВЕРСИЯ ДЛЯ АДМИНА: все пары =====
admin = result.copy()
admin.to_excel(os.path.join(PROCESSED, 'Перераспределение_админ.xlsx'), index=False)
print(f'\nДля админа: {len(admin)} строк')

# ===== ВЕРСИЯ ДЛЯ КЛАДОВЩИКА: одна пара на отправителя =====
# Берём первого получателя (лучший приоритет) для каждой пары (Откуда, Код)
kladovshik = result.drop_duplicates(subset=['Откуда', 'Код'], keep='first')

kladovshik.to_excel(os.path.join(PROCESSED, 'Перераспределение_кладовщик.xlsx'), index=False)
print(f'Для кладовщика: {len(kladovshik)} строк')

print('\nПример для админа:')
print(admin[['Откуда', 'Код', 'Наименование', 'Куда', 'РасходТам', 'ОстатокТам', 'Дефицит', 'СколькоПереместить']].head(10))

print('\nПример для кладовщика:')
print(kladovshik[['Откуда', 'Код', 'Наименование', 'Куда', 'РасходТам', 'ОстатокТам', 'Дефицит', 'СколькоПереместить']].head(10))