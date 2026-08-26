import streamlit as st
import sqlite3
import pandas as pd
import os

DB_PATH = r'C:\Users\92585\Desktop\Sklad_System\data\sklad.db'

st.set_page_config(page_title='Управление запасами', layout='wide')

st.title('🚚 Управление товарными запасами')

conn = sqlite3.connect(DB_PATH)

sto_list = pd.read_sql('SELECT DISTINCT СТО FROM Модель ORDER BY СТО', conn)['СТО'].tolist()

# Сохраняем выбранную СТО
if 'selected_sto' not in st.session_state:
    st.session_state.selected_sto = sto_list[0]

selected_sto = st.selectbox('Выберите СТО:', sto_list, key='selected_sto')

if 'prev_sto' not in st.session_state:
    st.session_state.prev_sto = selected_sto

if st.session_state.prev_sto != selected_sto:
    for key in ['editor_cs', 'editor_izl', 'editor_order']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.prev_sto = selected_sto
    st.session_state.show = False

if st.button('Показать рекомендации'):
    st.session_state.show = True

if 'show' in st.session_state and st.session_state.show:
    
    st.header(f'Рекомендации для: {selected_sto}')
    
    # 1. Переместить с ЦС
    query_cs = f'''
    SELECT Артикул, Наименование, ОстатокСТО, ОстатокЦС, СвободноЦС, НужноПереместить
    FROM Модель
    WHERE СТО = '{selected_sto}' AND Зона = 'Крит' AND НужноПереместить > 0
    ORDER BY НужноПереместить DESC
    LIMIT 20
    '''
    df_cs = pd.read_sql(query_cs, conn)
    df_cs['Заказать'] = 0
    st.subheader('📦 Переместить с ЦС')
    edited_cs = st.data_editor(df_cs, width='stretch', key='editor_cs')
    
    # 2. Излишки на других СТО
    query_izl = f'''
    SELECT 
        m.Артикул, m.Наименование, m.СТО as Откуда, m.ИзлишекСверхЦели,
        our.ОстатокСТО as ОстатокНаНашейСТО, our.ДефицитДоЦели as Дефицит
    FROM Модель m
    JOIN Модель our ON m.Артикул = our.Артикул
    WHERE m.Зона = 'Избыток' AND m.СТО != '{selected_sto}' AND m.ИзлишекСверхЦели > 0
      AND our.СТО = '{selected_sto}' AND our.Зона = 'Крит'
    ORDER BY m.ИзлишекСверхЦели DESC
    LIMIT 20
    '''
    df_izl = pd.read_sql(query_izl, conn)
    df_izl['Забрать'] = 0
    st.subheader('🔄 Переместить с других СТО')
    edited_izl = st.data_editor(df_izl, width='stretch', key='editor_izl')
    
    # 3. Заказ поставщику
    query_order = f'''
    SELECT Артикул, Наименование, ДефицитДоЦели
    FROM Модель
    WHERE СТО = '{selected_sto}' AND Зона = 'Крит' AND СвободноЦС = 0
      AND Код NOT IN (SELECT DISTINCT Код FROM Модель WHERE Зона = 'Избыток' AND СТО != '{selected_sto}')
    ORDER BY ДефицитДоЦели DESC
    LIMIT 20
    '''
    df_order = pd.read_sql(query_order, conn)
    df_order['Заказать'] = 0
    st.subheader('🛒 Заказать у поставщика')
    edited_order = st.data_editor(df_order, width='stretch', key='editor_order')

    # Кнопка сохранения
    if st.button('💾 Сохранить заказ'):
        output_path = r'C:\Users\92585\Desktop\Sklad_System\output'
        os.makedirs(output_path, exist_ok=True)
        
        file_name = f'Заказ_{selected_sto}.xlsx'
        file_path = os.path.join(output_path, file_name)
        
        with pd.ExcelWriter(file_path) as writer:
            if len(edited_cs[edited_cs['Заказать'] > 0]) > 0:
                edited_cs[edited_cs['Заказать'] > 0].to_excel(writer, sheet_name='С ЦС', index=False)
            if len(edited_izl[edited_izl['Забрать'] > 0]) > 0:
                edited_izl[edited_izl['Забрать'] > 0].to_excel(writer, sheet_name='С других СТО', index=False)
            if len(edited_order[edited_order['Заказать'] > 0]) > 0:
                edited_order[edited_order['Заказать'] > 0].to_excel(writer, sheet_name='Поставщик', index=False)
        
        st.success(f'Заказ сохранён: {file_path}')
    
    # 4. Зоны
    query_zones = f'''
    SELECT Зона, COUNT(*) as Позиций
    FROM Модель
    WHERE СТО = '{selected_sto}'
    GROUP BY Зона
    '''
    df_zones = pd.read_sql(query_zones, conn)
    st.subheader('📊 Распределение по зонам')
    st.bar_chart(df_zones.set_index('Зона'))

conn.close()