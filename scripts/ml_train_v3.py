import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, 'ML_Dataset_v3.xlsx'))
df['Дата'] = pd.to_datetime(df['Дата'])

# Убираем строки с NaN в лагах
df = df.dropna(subset=['Расход_Лаг1', 'Расход_Лаг12'])

# One-hot encoding для ТипСТО и ГруппаТовара
df = pd.get_dummies(df, columns=['ТипСТО', 'ГруппаТовара'], prefix=['Тип', 'Группа'])

# Признаки
features = [c for c in df.columns if c not in ['Код', 'Дата', 'Месяц', 'Расход', 'Артикул']]

X = df[features]
y = df['Расход']

# Разделяем по времени
split_date = df['Дата'].max() - pd.DateOffset(months=6)
X_train = X[df['Дата'] < split_date]
y_train = y[df['Дата'] < split_date]
X_test = X[df['Дата'] >= split_date]
y_test = y[df['Дата'] >= split_date]

print(f'Train: {len(X_train)}, Test: {len(X_test)}')
print(f'Признаков: {len(features)}')

model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'\n=== РЕЗУЛЬТАТЫ v3 ===')
print(f'MAE: {mae:.2f}')
print(f'R²: {r2:.4f}')

print('\n=== СРАВНЕНИЕ ===')
print(f'v2: MAE = 29.53, R² = 0.8409')
print(f'v3: MAE = {mae:.2f}, R² = {r2:.4f}')
print(f'Прирост R²: {(r2 - 0.8409)*100:+.2f}%')

importance = pd.DataFrame({
    'Признак': features,
    'Важность': model.feature_importances_
}).sort_values('Важность', ascending=False).head(20)

print('\nТоп-20 признаков:')
print(importance)