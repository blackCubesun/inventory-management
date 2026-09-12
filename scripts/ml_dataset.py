import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем плоскую оборотку
df_oborot = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_3года_плоский.xlsx'))

# Словарь месяцев → номер
months_map = {
    'Январь': 1, 'Февраль': 2, 'Март': 3, 'Апрель': 4, 'Май': 5, 'Июнь': 6,
    'Июль': 7, 'Август': 8, 'Сентябрь': 9, 'Октябрь': 10, 'Ноябрь': 11, 'Декабрь': 12
}

def parse_month(s):
    parts = str(s).replace(' г', '').split()
    if len(parts) == 2:
        return pd.Timestamp(year=int(parts[1]), month=months_map[parts[0]], day=1)
    return None

df_oborot['Дата'] = df_oborot['Месяц'].apply(parse_month)
df_oborot = df_oborot.dropna(subset=['Дата'])

# Агрегация по Код + Месяц (сумма по всем СТО)
df_agg = df_oborot.groupby(['Код', 'Дата']).agg({
    'Расход': 'sum'
}).reset_index()

print(f'Уникальных Код: {df_agg["Код"].nunique()}')
print(f'Уникальных дат: {df_agg["Дата"].nunique()}')
print(f'Всего строк: {len(df_agg)}')
print(df_agg.head(10))

df_agg.to_excel(os.path.join(PROCESSED, 'ML_РасходПоМесяцам.xlsx'), index=False)
print('\nСохранено: ML_РасходПоМесяцам.xlsx')