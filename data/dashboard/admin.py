import streamlit as st
import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'
V2_PATH = os.path.join(PROCESSED, 'Модель_v2.xlsx')

st.set_page_config(page_title='Админ-панель', layout='wide')

@st.cache_data
def load_data():
    df = pd.read_excel(V2_PATH, sheet_name='Расчёт')
    df['Код'] = df['Код'].astype(str).str.zfill(8)
    
    obshiy = df.groupby('Код')['Расход12мес'].sum().reset_index()
    obshiy.columns = ['Код', 'ОбщийРасходПоКомпании']
    df = df.merge(obshiy, on='Код', how='left')
    
    df['ГлобальныйНеликвид'] = (
        (df['ОбщийРасходПоКомпании'] == 0) & (df['ОстатокСТО'] > 0)
    )
    return df

df = load_data()

st.title('🔧 Админ-панель: Управление запасами')
st.markdown('---')

# ===== ВЕРХНИЕ МЕТРИКИ =====
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('Всего позиций', f'{len(df):,}')
with col2:
    st.metric('Остаток на СТО', f'{df["ОстатокСТО"].sum():,.0f} шт')
with col3:
    st.metric('Глобальный неликвид', f'{df[df["ГлобальныйНеликвид"]]["ОстатокСТО"].sum():,.0f} шт')

st.markdown('---')

# ===== ВЫБОР СТО =====
st.header('🏢 Разворот по СТО')

sto_list = ['ВСЕ СТО'] + sorted(df['СТО'].dropna().unique().tolist())
selected_sto = st.selectbox('Выберите СТО:', sto_list, key='admin_sto')

df_sto = df.copy() if selected_sto == 'ВСЕ СТО' else df[df['СТО'] == selected_sto].copy()

st.markdown('---')

# ===== КАТЕГОРИИ (ЗОНЫ) =====
st.subheader('📊 Категории по зонам')

zone_cols = st.columns(5)
zones = ['Крит', 'Норма', 'Избыток', 'Неликвид', 'Без движения']

selected_zone = None
for i, zona in enumerate(zones):
    with zone_cols[i]:
        count = len(df_sto[df_sto['Зона'] == zona])
        if st.button(f'{zona}\n({count})', key=f'zona_{zona}', use_container_width=True):
            selected_zone = zona

# ===== КАТЕГОРИИ (ТИП СТО) =====
st.subheader('🚌 Категории по типу')

tip_cols = st.columns(3)
tips = ['Автобусы', 'Электробусы', 'Кузовной']

selected_tip = None
for i, tip in enumerate(tips):
    with tip_cols[i]:
        count = len(df_sto[df_sto['ТипСТО'] == tip])
        if st.button(f'{tip}\n({count})', key=f'tip_{tip}', use_container_width=True):
            selected_tip = tip

# ===== ПРИМЕНЯЕМ ФИЛЬТРЫ =====
df_view = df_sto.copy()

if selected_zone:
    df_view = df_view[df_view['Зона'] == selected_zone]
    st.info(f'Фильтр: Зона = **{selected_zone}**')

if selected_tip:
    df_view = df_view[df_view['ТипСТО'] == selected_tip]
    st.info(f'Фильтр: ТипСТО = **{selected_tip}**')

# ===== ДОПОЛНИТЕЛЬНЫЕ ФИЛЬТРЫ =====
with st.expander('🔍 Дополнительные фильтры'):
    col1, col2 = st.columns(2)
    with col1:
        abc_filter = st.multiselect('ABC_XYZ', options=sorted(df_view['ABC_XYZ'].dropna().unique()))
    with col2:
        search = st.text_input('Поиск по наименованию')
    
    if abc_filter:
        df_view = df_view[df_view['ABC_XYZ'].isin(abc_filter)]
    if search:
        df_view = df_view[df_view['Наименование'].str.contains(search, case=False, na=False)]

st.markdown('---')

# ===== РЕЗУЛЬТАТ =====
st.subheader(f'📋 Позиции: {len(df_view):,}')

# Сводка
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
st.dataframe(
    df_view[[
        'СТО', 'Код', 'Наименование', 'ТипСТО', 'Зона', 'ABC_XYZ',
        'ОстатокСТО', 'ДоступныйОстаток', 'ТочкаЗаказа_СТО',
        'Расход12мес', 'ДнейХватит', 'НужноПереместитьЦС', 'ИзлишекКПеремещению'
    ]].sort_values('ОстатокСТО', ascending=False).head(500),
    width='stretch'
)

# Экспорт
csv = df_view.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    '💾 Скачать CSV',
    data=csv,
    file_name=f'admin_{selected_sto}.csv',
    mime='text/csv'
)