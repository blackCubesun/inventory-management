import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, '_Расчёт_v2_tochki.xlsx'))
df['Код'] = df['Код'].astype(str).str.zfill(8)

# Неликвид с остатком
nelikvid = df[(df['Расход12мес'] == 0) & (df['ОстатокСТО'] > 0)].copy()

# Все СТО с их потребностью
vse = df[['Код', 'СТО', 'ТипСТО', 'Расход12мес', 'ТочкаЗаказа_СТО', 'ДоступныйОстаток']].copy()
vse['Потребность'] = (vse['ТочкаЗаказа_СТО'] - vse['ДоступныйОстаток']).clip(lower=0)

# Нуждающиеся — где потребность > 0
nuzhda = vse[vse['Потребность'] >= 1].copy()

# Соединяем
result = nelikvid.merge(nuzhda, on='Код', how='inner', suffixes=('', '_Куда'))

# Сортируем: сначала самые нуждающиеся
result = result.sort_values(['Код', 'СТО', 'Потребность'], ascending=[True, True, False])

final_rows = []

for (otkuda, kod), group in result.groupby(['СТО', 'Код']):
    ostatok = group.iloc[0]['ОстатокСТО']
    if ostatok <= 0:
        continue
    
    for _, row in group.iterrows():
        if ostatok <= 0:
            break
        
        peremestit = min(ostatok, row['Потребность'])
        
        if peremestit >= 1:
            final_rows.append({
                'Откуда': otkuda,
                'Код': kod,
                'SKN': row['SKN'],
                'Артикул': row['Артикул'],
                'Наименование': row['Наименование'],
                'ТипСТО_Откуда': row['ТипСТО'],
                'ОстатокНаСТО': ostatok,
                'Куда': row['СТО_Куда'],
                'ТипСТО_Куда': row['ТипСТО_Куда'],
                'ПотребностьТам': row['Потребность'],
                'СколькоПереместить': round(peremestit, 1)
            })
            ostatok -= peremestit

final = pd.DataFrame(final_rows)
final = final.sort_values('СколькоПереместить', ascending=False)

print(f'Итоговая таблица: {len(final)}')
print(final[['Откуда', 'Код', 'Наименование', 'Куда', 'ПотребностьТам', 'СколькоПереместить']].head(20))

final.to_excel(os.path.join(PROCESSED, 'Перераспределение_v2.xlsx'), index=False)
print('\nСохранено: Перераспределение_v2.xlsx')