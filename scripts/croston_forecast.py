import pandas as pd
import numpy as np
import os
from sktime.forecasting.croston import Croston

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, 'ML_Dataset_v2.xlsx'))
df['Дата'] = pd.to_datetime(df['Дата'])

results = []

for (kod, tip), group in df.groupby(['Код', 'ТипСТО']):
    group = group.sort_values('Дата')
    ts = group['Расход'].values.astype(float)
    
    if len(ts) < 12:
        continue
    
    try:
        forecaster = Croston(smoothing=0.1)
        forecaster.fit(ts)
        forecast_value = float(forecaster.predict(fh=[1])[0])
    except Exception:
        forecast_value = np.mean(ts[ts > 0]) if len(ts[ts > 0]) > 0 else 0
    
    results.append({
        'Код': kod,
        'ТипСТО': tip,
        'Croston_Прогноз': round(forecast_value, 2),
        'СреднийРасход': round(np.mean(ts), 2),
        'СреднийНенулевой': round(np.mean(ts[ts > 0]), 2) if len(ts[ts > 0]) > 0 else 0,
        'КоличествоМесяцев': len(ts)
    })

df_croston = pd.DataFrame(results)
print(f'Позиций: {len(df_croston)}')
print(df_croston.head(20))

df_croston.to_excel(os.path.join(PROCESSED, 'Croston_Прогноз.xlsx'), index=False)
print('\nСохранено: Croston_Прогноз.xlsx')

df = pd.read_excel(os.path.join(PROCESSED, 'Croston_Прогноз.xlsx'))

# Позиции с редким спросом
df['Редкость'] = df['КоличествоМесяцев'] / 37

rare = df[df['Редкость'] < 0.7].sort_values('Редкость')
print('Редкие позиции (топ-20):')
print(rare.head(20))

print(f'\nВсего редких: {len(rare)}')