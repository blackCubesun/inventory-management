import pandas as pd
import numpy as np
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем прогнозы
df_worst = pd.read_excel(os.path.join(PROCESSED, 'Прогноз_ХудшийСценарий.xlsx'))
df_worst['Код'] = df_worst['Код'].astype(str).str.zfill(8)

# Параметры
LEAD_TIME_CS = 14  # дней (ЦС → СТО)
LEAD_TIME_STO = 1  # дней (внутри СТО)
Z_95 = 1.65        # 95% уровень сервиса
Z_99 = 2.33        # 99% уровень сервиса

# Прогноз на день (по среднему)
df_worst['Прогноз_НаДень'] = df_worst['Средний'] / 30

# СтОткл на день
df_worst['СтОткл_НаДень'] = df_worst['СтОткл'] / np.sqrt(30)

# Страховой запас = Z × σ × √(LeadTime)
df_worst['СтраховойЗапас_ЦС'] = (Z_95 * df_worst['СтОткл_НаДень'] * np.sqrt(LEAD_TIME_CS)).round(1)
df_worst['СтраховойЗапас_СТО'] = (Z_95 * df_worst['СтОткл_НаДень'] * np.sqrt(LEAD_TIME_STO)).round(1)

# Точка заказа = прогноз за LeadTime + страховой запас
df_worst['ТочкаЗаказа_ЦС'] = (df_worst['Прогноз_НаДень'] * LEAD_TIME_CS + df_worst['СтраховойЗапас_ЦС']).round(1)
df_worst['ТочкаЗаказа_СТО'] = (df_worst['Прогноз_НаДень'] * LEAD_TIME_STO + df_worst['СтраховойЗапас_СТО']).round(1)

# Для критичных позиций используем P90 как базовый прогноз
df_worst['ТочкаЗаказа_ЦС_P90'] = (df_worst['P90'] / 30 * LEAD_TIME_CS + df_worst['СтраховойЗапас_ЦС']).round(1)

print(df_worst.head(20))

df_worst.to_excel(os.path.join(PROCESSED, 'ТочкиЗаказа.xlsx'), index=False)
print('\nСохранено: ТочкиЗаказа.xlsx')