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
    
    # 1. Нормализация
    run('normalize_all.py')
    
    # 2. Модель
    run('model.py')
    
    # 3. Загрузка в базу
    run('db_load.py')
    
    # 4. Сохранение модели в базу
    run('db_save_model.py')
    
    print('\n🎉 ПОЛНЫЙ ЦИКЛ ЗАВЕРШЁН')