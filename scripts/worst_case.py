import pandas as pd
import numpy as np
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, 'ML_Dataset_v2.xlsx'))
df['Дата'] = pd.to_datetime(df['Дата'])

results = []

for (kod, tip), group in df.groupby(['Код', 'ТипСТО']):
    ts = group['Расход'].values.astype(float)
    
    if len(ts) < 6:
        continue
    
    results.append({
        'Код': kod,
        'ТипСТО': tip,
        'Средний': round(np.mean(ts), 2),
        'Медиана': round(np.median(ts), 2),
        'P75': round(np.percentile(ts, 75), 2),
        'P90': round(np.percentile(ts, 90), 2),
        'P95': round(np.percentile(ts, 95), 2),
        'Максимум': round(np.max(ts), 2),
        'СтОткл': round(np.std(ts), 2),
        'ВсегоМесяцев': len(ts)
    })

df_worst = pd.DataFrame(results)
print(f'Позиций: {len(df_worst)}')
print(df_worst.head(20))

df_worst.to_excel(os.path.join(PROCESSED, 'Прогноз_ХудшийСценарий.xlsx'), index=False)
print('\nСохранено: Прогноз_ХудшийСценарий.xlsx')