import math
import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

def load_model():
    return pd.read_excel(os.path.join(PROCESSED, 'Модель.xlsx'))

def get_recommendations(df, sto_name):
    df_sto = df[df['СТО'] == sto_name].copy()
    
    # Все позиции в Крите на этой СТО
    krit = df_sto[df_sto['Зона'] == 'Крит'].copy()
    krit['Дефицит'] = krit['ЦелевойЗапасШт'] - krit['ДоступныйОстаток']
    krit = krit[krit['Дефицит'] > 0]
    
    # ===== 1. ПЕРЕМЕСТИТЬ С ЦС =====
    move_cs = krit[krit['СвободноЦС'] > 0].copy()
    move_cs['Объём'] = move_cs[['Дефицит', 'СвободноЦС']].min(axis=1)
    move_cs = move_cs[move_cs['Дефицит'] >= 1]  # только реальный дефицит от 1
    move_cs['Объём'] = move_cs['Объём'].apply(math.ceil)
    move_cs = move_cs[['Код', 'SKN', 'Наименование', 'ОстатокСТО', 'Дефицит', 'СвободноЦС', 'Объём']]
    
    # ===== 2. ПЕРЕМЕСТИТЬ С ДРУГИХ СТО =====
    # Сначала считаем, сколько дефицита осталось после ЦС по каждому Коду
    remaining = {}
    for _, row in krit.iterrows():
        code = row['Код']
        deficit = row['Дефицит']
        cs_cover = move_cs[move_cs['Код'] == code]['Объём'].sum() if len(move_cs) > 0 else 0
        remaining[code] = max(0, deficit - cs_cover)
    
    # Излишки на других СТО
    izl_pool = df[
        (df['Зона'] == 'Избыток') & 
        (df['СТО'] != sto_name) &
        (df['ИзлишекСверхЦели'] > 0)
    ].copy()
    
    rows = []
    for _, izl in izl_pool.iterrows():
        code = izl['Код']
        if code in remaining and remaining[code] > 0:
            volume = min(izl['ИзлишекСверхЦели'], remaining[code])
            if volume >= 1:
                volume = math.ceil(volume)
                our_row = krit[krit['Код'] == code].iloc[0]
                rows.append({
                    'Код': code,
                    'SKN': izl['SKN'],
                    'Откуда': izl['СТО'],
                    'Наименование': izl['Наименование'],
                    'ДефицитСТО': our_row['Дефицит'],
                    'Излишек': izl['ИзлишекСверхЦели'],
                    'Объём': volume,
                    'ОсталосьПокрыть': max(0, remaining[code] - volume)
                })
                remaining[code] -= volume
    
    izl_others = pd.DataFrame(rows)
    if len(izl_others) > 0:
        izl_others = izl_others.sort_values('Объём', ascending=False)
    
    # ===== 3. ЗАКАЗАТЬ У ПОСТАВЩИКА =====
    order_rows = []
    for _, row in krit.iterrows():
        code = row['Код']
        deficit = row['Дефицит']
        cs_cover = move_cs[move_cs['Код'] == code]['Объём'].sum() if len(move_cs) > 0 else 0
        izl_cover = izl_others[izl_others['Код'] == code]['Объём'].sum() if len(izl_others) > 0 else 0
        covered = cs_cover + izl_cover
        if covered < deficit:
            raw_deficit = deficit - covered
            to_order = math.ceil(raw_deficit)
            order_type = 'Срочный' if raw_deficit >= 1 else 'Возможный'
            if to_order >= 1:
                order_rows.append({
                    'Код': code,
                    'SKN': row['SKN'],
                    'Наименование': row['Наименование'],
                    'Дефицит': deficit,
                    'Покрыто': covered,
                    'Заказать': to_order,
                    'Тип': order_type,
                })
    
    order = pd.DataFrame(order_rows)
    if len(order) > 0:
        order = order.sort_values('Заказать', ascending=False)

    return move_cs, izl_others, order

if __name__ == '__main__':
    df = load_model()
    
    sto_list = sorted(df['СТО'].unique())
    print('Доступные СТО:')
    for i, sto in enumerate(sto_list, 1):
        print(f'{i}. {sto}')
    
    num = int(input('\nВведи номер СТО: '))
    sto_name = sto_list[num - 1]
    
    move_cs, izl_others, order = get_recommendations(df, sto_name)
    
    print(f'\n=== РЕКОМЕНДАЦИИ ДЛЯ: {sto_name} ===')
    
    print(f'\n1. ПЕРЕМЕСТИТЬ С ЦС ({len(move_cs)} позиций):')
    if len(move_cs) > 0:
        print(move_cs.head(15))
    
    print(f'\n2. ПЕРЕМЕСТИТЬ С ДРУГИХ СТО ({len(izl_others)} позиций):')
    if len(izl_others) > 0:
        print(izl_others.head(15))
    
    print(f'\n3. ЗАКАЗАТЬ У ПОСТАВЩИКА ({len(order)} позиций):')
    if len(order) > 0:
        urgent = order[order['Тип'] == 'Срочный']
        possible = order[order['Тип'] == 'Возможный']
        
        print(f'\n   Срочный заказ ({len(urgent)} позиций):')
        if len(urgent) > 0:
            print(urgent[['Код', 'SKN', 'Наименование', 'Заказать']].head(15))
        
        print(f'\n   Возможный заказ ({len(possible)} позиций):')
        if len(possible) > 0:
            print(possible[['Код', 'SKN', 'Наименование', 'Заказать']].head(15))
    else:
        print('Нет позиций для заказа')