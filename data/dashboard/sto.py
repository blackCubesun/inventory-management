import streamlit as st
import pandas as pd
import os
from datetime import datetime

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'
OUTPUT = r'C:\Users\92585\Desktop\Sklad_System\output'
V2_PATH = os.path.join(PROCESSED, 'Модель_v2.xlsx')

st.set_page_config(page_title='Панель СТО', layout='wide')

@st.cache_data
def load_raschet():
    df = pd.read_excel(V2_PATH, sheet_name='Расчёт')
    df['Код'] = df['Код'].astype(str).str.zfill(8)
    return df

@st.cache_data
def load_pereras():
    df = pd.read_excel(V2_PATH, sheet_name='Перераспределение')
    df['Код'] = df['Код'].astype(str).str.zfill(8)
    return df

df = load_raschet()
df_per = load_pereras()

st.title('📦 Панель кладовщика')
st.markdown('---')

# ===== ВЫБОР СТО =====
sto_list = sorted(df['СТО'].dropna().unique())

if 'selected_sto' not in st.session_state:
    st.session_state.selected_sto = sto_list[0]

selected_sto = st.selectbox('Выберите вашу СТО:', sto_list, key='selected_sto')

# Сброс при смене СТО
if 'prev_sto' not in st.session_state:
    st.session_state.prev_sto = selected_sto

if st.session_state.prev_sto != selected_sto:
    for key in ['editor_cs', 'editor_izl']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.prev_sto = selected_sto

# ===== ФИЛЬТР ПО СТО =====
df_sto = df[df['СТО'] == selected_sto].copy()
df_per_sto = df_per[df_per['Куда'] == selected_sto].copy()

st.markdown('---')

# ===== МЕТРИКИ =====
col1, col2, col3, col4 = st.columns(4)

with col1:
    krit = len(df_sto[df_sto['Зона'] == 'Крит'])
    st.metric('🔴 Крит', krit)

with col2:
    norma = len(df_sto[df_sto['Зона'] == 'Норма'])
    st.metric('🟢 Норма', norma)

with col3:
    izl = len(df_sto[df_sto['Зона'] == 'Избыток'])
    st.metric('🟡 Избыток', izl)

with col4:
    per = len(df_per_sto)
    st.metric('🔄 Переместить', per)

st.markdown('---')

# ===== КНОПКА ПОКАЗАТЬ =====
if st.button('🔍 Показать рекомендации', use_container_width=True):
    st.session_state.show_recs = True

if st.session_state.get('show_recs', False):
    
    # ===== 1. ЗАКАЗАТЬ С ЦС =====
    st.header('📦 1. Заказать с ЦС')
    
    cs = df_sto[(df_sto['Зона'] == 'Крит') & (df_sto['НужноПереместитьЦС'] >= 1)].copy()
    cs = cs.sort_values('НужноПереместитьЦС', ascending=False)
    
    if len(cs) > 0:
        st.write(f'Позиций: **{len(cs)}** | Всего штук: **{cs["НужноПереместитьЦС"].sum():,.0f}**')
        
        cs_view = cs[['Код', 'Наименование', 'ОстатокСТО', 'ТочкаЗаказа_СТО', 'НужноПереместитьЦС']].copy()
        cs_view = cs_view.rename(columns={'НужноПереместитьЦС': 'Рекомендуем'})
        cs_view['Заказать'] = 0
        
        edited_cs = st.data_editor(cs_view, width='stretch', key='editor_cs', height=400)
    else:
        st.info('Нет позиций для заказа с ЦС')
        edited_cs = pd.DataFrame()
    
    st.markdown('---')
    
    # ===== 2. ЗАБРАТЬ У ДРУГИХ СТО =====
    st.header('🔄 2. Забрать у других СТО')
    
    if len(df_per_sto) > 0:
        st.write(f'Рекомендаций: **{len(df_per_sto)}** | Всего штук: **{df_per_sto["СколькоПереместить"].sum():,.0f}**')
        
        per_view = df_per_sto[['Откуда', 'Код', 'Наименование', 'ОстатокНаСТО', 'СколькоПереместить']].copy()
        per_view = per_view.rename(columns={'СколькоПереместить': 'Рекомендуем'})
        per_view['Забрать'] = 0
        
        edited_izl = st.data_editor(per_view, width='stretch', key='editor_izl', height=400)
    else:
        st.info('Нет рекомендаций по перераспределению')
        edited_izl = pd.DataFrame()
    
    st.markdown('---')
    
    # ===== 3. СОХРАНЕНИЕ ЗАКАЗА =====
    st.header('💾 3. Сохранить заказ')
    
    if st.button('💾 Сохранить заказ в XLSX', use_container_width=True):
        os.makedirs(OUTPUT, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        safe_sto = selected_sto.replace(' ', '_').replace('(', '').replace(')', '')
        file_name = f'Заказ_{safe_sto}_{timestamp}.xlsx'
        file_path = os.path.join(OUTPUT, file_name)
        
        with pd.ExcelWriter(file_path) as writer:
            # Заказ с ЦС
            if len(edited_cs) > 0:
                order_cs = edited_cs[edited_cs['Заказать'] > 0]
                if len(order_cs) > 0:
                    order_cs.to_excel(writer, sheet_name='С ЦС', index=False)
            
            # Забрать у других СТО
            if len(edited_izl) > 0:
                order_izl = edited_izl[edited_izl['Забрать'] > 0]
                if len(order_izl) > 0:
                    order_izl.to_excel(writer, sheet_name='С других СТО', index=False)
        
        st.success(f'✅ Заказ сохранён: {file_path}')
        st.info('Файл можно отправить в ЦС для формирования перемещения')