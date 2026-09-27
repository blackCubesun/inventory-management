import streamlit as st
import pandas as pd
import os
from datetime import datetime

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'
OUTPUT = r'C:\Users\92585\Desktop\Sklad_System\output'
V2_PATH = os.path.join(PROCESSED, 'Модель_v2.xlsx')

st.set_page_config(page_title='Админ-панель v2', layout='wide')

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

st.title('🔧 Админ-панель v2')
st.markdown('---')

tab1, tab2, tab3 = st.tabs(['📊 Расчёт', '🔄 Перераспределение', '📋 Свод'])

# ============================================================
# ВКЛАДКА 1: РАСЧЁТ
# ============================================================
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Всего позиций', f'{len(df):,}')
    with col2:
        st.metric('СТО', f'{df["СТО"].nunique()}')
    with col3:
        st.metric('Востребован', f'{df["Востребован"].sum():,}')
    with col4:
        st.metric('Глобальный неликвид', f'{df["ГлобальныйНеликвид"].sum():,}')
    
    st.markdown('---')
    
    # Кнопки категорий
    if 'selected_zona' not in st.session_state:
        st.session_state.selected_zona = None
    
    categories = [
        'Все позиции',
        'Крит', 'Норма', 'Избыток', 
        'Неликвид (локальный)',
        'Востребован',
        'Глобальный неликвид',
        'Без движения'
    ]
    cols = st.columns(len(categories))
    
    for i, cat in enumerate(categories):
        with cols[i]:
            if cat == 'Все позиции':
                count = len(df)
            elif cat == 'Востребован':
                count = df['Востребован'].sum()
            elif cat == 'Глобальный неликвид':
                count = df['ГлобальныйНеликвид'].sum()
            elif cat == 'Неликвид (локальный)':
                count = len(df[df['Зона'] == 'Неликвид'])
            else:
                count = len(df[df['Зона'] == cat])
            
            if st.button(f'{cat}\n({count})', key=f'cat_{cat}', use_container_width=True):
                st.session_state.selected_zona = cat
    
    selected = st.session_state.selected_zona
    
    # Фильтры
    st.markdown('---')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        sto_filter = st.multiselect('СТО', sorted(df['СТО'].dropna().unique()), key='sto_f')
    with col2:
        tip_filter = st.multiselect('Тип СТО', sorted(df['ТипСТО'].dropna().unique()), key='tip_f')
    with col3:
        abc_filter = st.multiselect('ABC_XYZ', sorted(df['ABC_XYZ'].dropna().unique()), key='abc_f')
    with col4:
        gruppa_filter = st.multiselect('ГруппаТовара', sorted(df['ГруппаТовара'].dropna().unique()), key='gr_f')
    
    # Применяем
    df_view = df.copy()
    if selected and selected != 'Все позиции':
        if selected == 'Востребован':
            df_view = df_view[df_view['Востребован'] == 1]
        elif selected == 'Глобальный неликвид':
            df_view = df_view[df_view['ГлобальныйНеликвид'] == 1]
        elif selected == 'Неликвид (локальный)':
            df_view = df_view[df_view['Зона'] == 'Неликвид']
        else:
            df_view = df_view[df_view['Зона'] == selected]
    
    if sto_filter:
        df_view = df_view[df_view['СТО'].isin(sto_filter)]
    if tip_filter:
        df_view = df_view[df_view['ТипСТО'].isin(tip_filter)]
    if abc_filter:
        df_view = df_view[df_view['ABC_XYZ'].isin(abc_filter)]
    if gruppa_filter:
        df_view = df_view[df_view['ГруппаТовара'].isin(gruppa_filter)]
    
    if selected:
        st.success(f'Категория: **{selected}**')
    st.write(f'Отфильтровано: **{len(df_view):,}** позиций')
    
    # Метрики
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Позиций', f'{len(df_view):,}')
    with col2:
        st.metric('Остаток', f'{df_view["ОстатокСТО"].sum():,.0f} шт')
    with col3:
        st.metric('Нужно с ЦС', f'{df_view["НужноПереместитьЦС"].sum():,.0f} шт')
    with col4:
        st.metric('Излишек', f'{df_view["ИзлишекКПеремещению"].sum():,.0f} шт')
    
    # Таблица
    st.markdown('---')
    columns_to_show = [
        'СТО', 'Код', 'Наименование', 'ТипСТО', 'ГруппаТовара', 'Зона', 'ABC_XYZ',
        'ОстатокСТО', 'ДоступныйОстаток', 'ТочкаЗаказа_СТО',
        'Расход12мес', 'ДнейХватит', 'Востребован', 'ГлобальныйНеликвид'
    ]
    st.dataframe(df_view[columns_to_show].sort_values('ОстатокСТО', ascending=False).head(1000),
                 width='stretch', height=500)
    
    # Сохранение
    st.markdown('---')
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button('💾 Сохранить в XLSX', key='save_raschet'):
            os.makedirs(OUTPUT, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            file_name = f'Расчёт_{selected or "all"}_{timestamp}.xlsx'
            file_path = os.path.join(OUTPUT, file_name)
            df_view.to_excel(file_path, index=False)
            st.success(f'Сохранено: {file_path}')
    with col2:
        csv = df_view.to_csv(index=False).encode('utf-8-sig')
        st.download_button('💾 Скачать CSV', data=csv, file_name='raschet.csv', mime='text/csv')

# ============================================================
# ВКЛАДКА 2: ПЕРЕРАСПРЕДЕЛЕНИЕ
# ============================================================
with tab2:
    st.header('🔄 Перераспределение между СТО')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Всего рекомендаций', f'{len(df_per):,}')
    with col2:
        st.metric('Отправителей', f'{df_per["Откуда"].nunique()}')
    with col3:
        st.metric('Получателей', f'{df_per["Куда"].nunique()}')
    
    st.markdown('---')
    
    # Фильтры
    col1, col2, col3 = st.columns(3)
    with col1:
        otkuda_filter = st.multiselect('Откуда', sorted(df_per['Откуда'].dropna().unique()), key='otk_f')
    with col2:
        kuda_filter = st.multiselect('Куда', sorted(df_per['Куда'].dropna().unique()), key='kud_f')
    with col3:
        tip_filter2 = st.multiselect('Тип СТО (откуда)', sorted(df_per['ТипСТО_Откуда'].dropna().unique()), key='tip_f2')
    
    df_per_view = df_per.copy()
    if otkuda_filter:
        df_per_view = df_per_view[df_per_view['Откуда'].isin(otkuda_filter)]
    if kuda_filter:
        df_per_view = df_per_view[df_per_view['Куда'].isin(kuda_filter)]
    if tip_filter2:
        df_per_view = df_per_view[df_per_view['ТипСТО_Откуда'].isin(tip_filter2)]
    
    st.write(f'Отфильтровано: **{len(df_per_view):,}** рекомендаций')
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Всего к перемещению', f'{df_per_view["СколькоПереместить"].sum():,.0f} шт')
    with col2:
        st.metric('Уникальных позиций', f'{df_per_view["Код"].nunique()}')
    
    st.markdown('---')
    st.dataframe(
        df_per_view[[
            'Откуда', 'Код', 'Наименование', 'ТипСТО_Откуда', 'ОстатокНаСТО',
            'Куда', 'ТипСТО_Куда', 'РасходТам', 'ОстатокТам', 'Дефицит', 'СколькоПереместить'
        ]].sort_values('СколькоПереместить', ascending=False).head(1000),
        width='stretch', height=500
    )
    
    # Сохранение
    st.markdown('---')
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button('💾 Сохранить в XLSX', key='save_per'):
            os.makedirs(OUTPUT, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            file_path = os.path.join(OUTPUT, f'Перераспределение_{timestamp}.xlsx')
            df_per_view.to_excel(file_path, index=False)
            st.success(f'Сохранено: {file_path}')
    with col2:
        csv = df_per_view.to_csv(index=False).encode('utf-8-sig')
        st.download_button('💾 Скачать CSV', data=csv, file_name='pereraspredelenie.csv', mime='text/csv')

# ============================================================
# ВКЛАДКА 3: СВОД
# ============================================================
with tab3:
    st.header('📋 Свод по СТО')
    
    pivot = df.pivot_table(
        index='СТО',
        columns='Зона',
        values='Код',
        aggfunc='count',
        fill_value=0
    )
    st.subheader('Позиции по СТО и зонам')
    st.dataframe(pivot, width='stretch')
    
    st.markdown('---')
    
    if 'ГруппаТовара' in df.columns:
        pivot2 = df.pivot_table(
            index='СТО',
            columns='ГруппаТовара',
            values='Код',
            aggfunc='count',
            fill_value=0
        )
        st.subheader('Позиции по СТО и группам')
        st.dataframe(pivot2, width='stretch')
    
    st.markdown('---')
    
    # Свод по востребованности
    st.subheader('Неликвид: востребован vs глобальный')
    
    nelikvid_svod = df[df['Зона'] == 'Неликвид'].groupby('СТО').agg({
        'Код': 'count',
        'Востребован': 'sum',
        'ГлобальныйНеликвид': 'sum',
        'ОстатокСТО': 'sum'
    }).round(0)
    nelikvid_svod.columns = ['ВсегоНеликвида', 'Востребован', 'Глобальный', 'ОстатокШт']
    st.dataframe(nelikvid_svod, width='stretch')