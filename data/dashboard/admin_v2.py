import streamlit as st
import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'
V2_PATH = os.path.join(PROCESSED, 'Модель_v2.xlsx')

st.set_page_config(page_title='Админ-панель v2', layout='wide')

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

st.title('🔧 Админ-панель v2')
st.markdown('---')

# ===== МЕТРИКИ =====
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('Всего позиций', f'{len(df):,}')
with col2:
    st.metric('СТО', f'{df["СТО"].nunique()}')
with col3:
    st.metric('Остаток на СТО', f'{df["ОстатокСТО"].sum():,.0f} шт')
with col4:
    global_net = df[df['ГлобальныйНеликвид']]['ОстатокСТО'].sum()
    st.metric('Глобальный неликвид', f'{global_net:,.0f} шт')

st.markdown('---')

# ===== ВЫБОР ЗОНЫ (кнопки) =====
st.header('📂 Выбор категории')

if 'selected_zona' not in st.session_state:
    st.session_state.selected_zona = None

zones_list = ['Все позиции', 'Крит', 'Норма', 'Избыток', 'Неликвид', 'Без движения', 'Глобальный неликвид']
cols = st.columns(len(zones_list))

for i, zona in enumerate(zones_list):
    with cols[i]:
        if zona == 'Все позиции':
            count = len(df)
        elif zona == 'Глобальный неликвид':
            count = df['ГлобальныйНеликвид'].sum()
        else:
            count = len(df[df['Зона'] == zona])
        
        if st.button(f'{zona}\n({count})', key=f'zona_{zona}', use_container_width=True):
            st.session_state.selected_zona = zona

selected_zona = st.session_state.selected_zona

# ===== ФИЛЬТРЫ =====
st.markdown('---')
st.header('🔍 Дополнительные фильтры')

col1, col2, col3 = st.columns(3)

with col1:
    sto_filter = st.multiselect('СТО', sorted(df['СТО'].dropna().unique()))
with col2:
    tip_filter = st.multiselect('Тип СТО', sorted(df['ТипСТО'].dropna().unique()))
with col3:
    abc_filter = st.multiselect('ABC_XYZ', sorted(df['ABC_XYZ'].dropna().unique()))

# ===== ПРИМЕНЯЕМ ФИЛЬТРЫ =====
df_view = df.copy()

if selected_zona and selected_zona != 'Все позиции':
    if selected_zona == 'Глобальный неликвид':
        df_view = df_view[df_view['ГлобальныйНеликвид']]
    else:
        df_view = df_view[df_view['Зона'] == selected_zona]

if sto_filter:
    df_view = df_view[df_view['СТО'].isin(sto_filter)]
if tip_filter:
    df_view = df_view[df_view['ТипСТО'].isin(tip_filter)]
if abc_filter:
    df_view = df_view[df_view['ABC_XYZ'].isin(abc_filter)]

# Показываем текущий фильтр
if selected_zona:
    st.success(f'Выбрана категория: **{selected_zona}**')
else:
    st.info('Категория не выбрана. Показаны все позиции.')

st.write(f'Отфильтровано: **{len(df_view):,}** позиций')

st.markdown('---')

# ===== МЕТРИКИ ПО ФИЛЬТРУ =====
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric('Позиций', f'{len(df_view):,}')
with col2:
    st.metric('Остаток', f'{df_view["ОстатокСТО"].sum():,.0f} шт')
with col3:
    st.metric('Нужно с ЦС', f'{df_view["НужноПереместитьЦС"].sum():,.0f} шт')
with col4:
    st.metric('Излишек', f'{df_view["ИзлишекКПеремещению"].sum():,.0f} шт')

st.markdown('---')

# ===== ТАБЛИЦА =====
st.header('📋 Позиции')

# Выбор столбцов для отображения
columns_to_show = [
    'СТО', 'Код', 'Наименование', 'ТипСТО', 'Зона', 'ABC_XYZ',
    'ОстатокСТО', 'ДоступныйОстаток', 'ТочкаЗаказа_СТО',
    'Расход12мес', 'ДнейХватит', 'НужноПереместитьЦС', 'ИзлишекКПеремещению'
]

st.dataframe(
    df_view[columns_to_show].sort_values('ОстатокСТО', ascending=False).head(1000),
    width='stretch',
    height=600
)

# ===== ЭКСПОРТ =====
st.markdown('---')
csv = df_view.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    '💾 Скачать CSV',
    data=csv,
    file_name=f'admin_{selected_zona or "all"}.csv',
    mime='text/csv'
)