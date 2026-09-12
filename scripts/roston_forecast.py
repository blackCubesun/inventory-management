import pandas as pd
import numpy as np
import os
from intermittent_forecast import croston

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

# Загружаем датасет
df = pd.read_excel(os.path.join(PROCESSED, 'ML_Dataset_v2.xlsx'))
df['Дата'] = pd.to_datetime(df['Дата'])

# Для каждого Код+ТипСТО применяем Croston/SBA
results = []

for (kod, tip), group in df.groupby(['Код', 'ТипСТО']):
    group = group.sort_values('Дата')
    ts = group['Расход'].values
    
    # Нужно минимум 24 точки для адекватного прогноза
    if len(ts) < 12:
        continue
    
    # SBA прогноз
    try:
        sba_forecast = croston(ts, method='sba', alpha=0.15)
        forecast_value = sba_forecast[-1] if not np.isnan(sba_forecast[-1]) else 0
    except Exception:
        forecast_value = 0
    
    results.append({
        'Код': kod,
        'ТипСТО': tip,
        'CrostonSBA_Прогноз': forecast_value,
        'СреднийРасход': np.mean(ts[ts > 0]) if len(ts[ts > 0]) > 0 else 0,
        'КоличествоМесяцев': len(ts)
    })

df_croston = pd.DataFrame(results)
print(f'Позиций: {len(df_croston)}')
print(df_croston.head(20))

df_croston.to_excel(os.path.join(PROCESSED, 'Croston_Прогноз.xlsx'), index=False)
print('\nСохранено: Croston_Прогноз.xlsx')