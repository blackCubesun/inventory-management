import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем оборотку
df_oborot = pd.read_excel(os.path.join(PROCESSED, 'Оборотка_3года_плоский.xlsx'))

# Загружаем справочник СТО
df_sto = pd.read_excel(os.path.join(PROCESSED, 'Справочник_СТО.xlsx'))

# Соединяем
df_oborot = df_oborot.merge(df_sto, on='СТО', how='left')

print('СТО без типа:')
print(df_oborot[df_oborot['ТипСТО'].isna()]['СТО'].unique())

# Парсим месяц
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

# Агрегация по Код + Дата + ТипСТО
df_agg = df_oborot.groupby(['Код', 'Дата', 'ТипСТО']).agg({
    'Расход': 'sum'
}).reset_index()

print(f'\nРазмер: {df_agg.shape}')
print(f'Уникальных типов: {df_agg["ТипСТО"].nunique()}')
print(df_agg.head(10))

df_agg.to_excel(os.path.join(PROCESSED, 'ML_РасходПоТипам.xlsx'), index=False)
print('\nСохранено: ML_РасходПоТипам.xlsx')