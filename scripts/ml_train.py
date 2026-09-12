import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, 'ML_Dataset.xlsx'))
df['Дата'] = pd.to_datetime(df['Дата'])

# Убираем строки с NaN в лагах
df = df.dropna(subset=['Расход_Лаг1', 'Расход_Лаг12'])

# Признаки
features = ['Температура', 'Давление', 'Влажность', 'Ветер', 'Осадки',
            'ПотреблениеТоплива', 'НомерМесяца', 'Год',
            'Расход_Лаг1', 'Расход_Лаг12', 'Расход_Среднее3']

X = df[features]
y = df['Расход']

# Разделяем: последние 6 месяцев — тест
split_date = df['Дата'].max() - pd.DateOffset(months=6)
X_train = X[df['Дата'] < split_date]
y_train = y[df['Дата'] < split_date]
X_test = X[df['Дата'] >= split_date]
y_test = y[df['Дата'] >= split_date]

print(f'Train: {len(X_train)}, Test: {len(X_test)}')

# Модель
model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Предсказание
y_pred = model.predict(X_test)

# Метрики
print(f'\nMAE: {mean_absolute_error(y_test, y_pred):.2f}')
print(f'R²: {r2_score(y_test, y_pred):.4f}')

# Важность признаков
importance = pd.DataFrame({
    'Признак': features,
    'Важность': model.feature_importances_
}).sort_values('Важность', ascending=False)

print('\nВажность признаков:')
print(importance)