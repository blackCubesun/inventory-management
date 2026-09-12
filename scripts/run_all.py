import subprocess
import sys
import os

BASE = r'C:\Users\92585\Desktop\Sklad_System\scripts'

def run(script):
    print(f'\n{"="*60}')
    print(f'ЗАПУСК: {script}')
    print(f'{"="*60}')
    result = subprocess.run([sys.executable, os.path.join(BASE, script)])
    if result.returncode != 0:
        print(f'❌ Ошибка в {script}')
        sys.exit(1)
    print(f'✅ {script} завершён')

if __name__ == '__main__':
    print('🚀 СТАРТ ПОЛНОГО ЦИКЛА ОБРАБОТКИ')
    
    # 1. Нормализация исходных отчётов
    run('normalize_all.py')
    
    # 2. Модель (старая)
    run('model.py')
    
    # 3. Погода
    run('normalize_pogoda.py')
    
    # 4. Пробег
    run('probeg_traektorii.py')
    run('probeg_monthly.py')
    
    # 5. Потребление
    run('potreblenie.py')
    
    # 6. ML-датасет
    run('ml_dataset_v2.py')
    run('ml_features_v2.py')
    
    # 7. Croston
    run('croston_manual.py')
    
    # 8. Худший сценарий
    run('worst_case.py')
    
    # 9. Точки заказа
    run('reorder_point.py')
    
    # 10. Модель v2
    run('fill_model_v2.py')
    
    # 11. База данных
    run('db_load.py')
    run('db_save_model.py')
    
    print('\n🎉 ПОЛНЫЙ ЦИКЛ ЗАВЕРШЁН')