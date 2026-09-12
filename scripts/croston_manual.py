import pandas as pd
import numpy as np
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, 'ML_Dataset_v2.xlsx'))
df['Дата'] = pd.to_datetime(df['Дата'])

def croston_sba(ts, alpha=0.1):
    """Классический Croston с SBA-коррекцией"""
    ts = np.array(ts, dtype=float)
    
    # Индексы ненулевых значений
    nonzero_idx = np.where(ts > 0)[0]
    if len(nonzero_idx) == 0:
        return 0.0
    
    # Размеры спроса (q) и интервалы (p)
    q = ts[nonzero_idx]
    
    # Интервалы между ненулевыми
    if len(nonzero_idx) > 1:
        p = np.diff(nonzero_idx)
    else:
        p = np.array([len(ts)])
    
    # Сглаживание
    q_hat = q[0]
    p_hat = p[0] if len(p) > 0 else 1
    
    for i in range(1, len(q)):
        q_hat = alpha * q[i] + (1 - alpha) * q_hat
    
    for i in range(len(p)):
        p_hat = alpha * p[i] + (1 - alpha) * p_hat
    
    # Прогноз Croston
    forecast = q_hat / p_hat if p_hat > 0 else 0
    
    # SBA-коррекция (убирает смещение)
    forecast_sba = forecast * (1 - alpha / 2)
    
    return forecast_sba


results = []

for (kod, tip), group in df.groupby(['Код', 'ТипСТО']):
    group = group.sort_values('Дата')
    ts = group['Расход'].values.astype(float)
    
    if len(ts) < 12:
        continue
    
    forecast = croston_sba(ts, alpha=0.1)
    
    results.append({
        'Код': kod,
        'ТипСТО': tip,
        'CrostonSBA': round(forecast, 2),
        'СреднийРасход': round(np.mean(ts), 2),
        'НенулевыхМесяцев': int((ts > 0).sum()),
        'ВсегоМесяцев': len(ts),
        'СреднийНенулевой': round(np.mean(ts[ts > 0]), 2) if (ts > 0).any() else 0
    })

df_croston = pd.DataFrame(results)
print(f'Позиций: {len(df_croston)}')
print(df_croston.head(20))

df_croston.to_excel(os.path.join(PROCESSED, 'Croston_Прогноз.xlsx'), index=False)
print('\nСохранено: Croston_Прогноз.xlsx')