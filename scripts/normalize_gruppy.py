import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

df = pd.read_excel(os.path.join(PROCESSED, 'Иерархия_товаров.xlsx'))

# Укрупнение групп
def get_big_group(roditel):
    r = str(roditel).lower()
    
    if 'убзс' in r:
        return 'УБЗС'
    if 'метиз' in r or 'фитинг' in r:
        return 'Метизы'
    if 'расходн' in r or 'автохим' in r or 'гсм' in r:
        return 'Расходники'
    if 'жгут' in r or 'провод' in r or 'освещ' in r or 'датчик' in r or 'выключател' in r or 'акб' in r:
        return 'Электрика'
    if 'инструмент' in r or 'диагностич' in r or 'оборудован' in r:
        return 'Инструмент'
    if 'хозтовар' in r or 'канцеляр' in r or 'мебел' in r or 'оргтехник' in r:
        return 'Хозтовары'
    if 'спецодежд' in r or 'сиз' in r:
        return 'Спецодежда'
    
    # Всё остальное — запчасти по узлам
    if any(x in r for x in ['запчаст', 'загрузк', 'автопарк', 'стекл', 'перегородк',
                             'поручн', 'шиномонтаж', 'фильтр', 'двер', 'сидень',
                             'кабин', 'охлажд', 'прибор', 'шин', 'диск', 'тормоз',
                             'двигател', 'вентиляц', 'отоплен', 'кондицион',
                             'рулев', 'пожарн', 'москвич', 'ответхран']):
        return 'Запчасти'
    
    return 'Прочее'

df['ГруппаТовара'] = df['Родитель'].apply(get_big_group)

print('Укрупнённые группы:')
print(df['ГруппаТовара'].value_counts())

df.to_excel(os.path.join(PROCESSED, 'Иерархия_товаров_укрупнённая.xlsx'), index=False)
print('\nСохранено: Иерархия_товаров_укрупнённая.xlsx')