import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============ CONFIGURACIÓN ============
st.set_page_config(
    page_title="Monitoreo Humanitario - Centroamérica",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ DATOS DE LOS PROYECTOS ============

# GT - Guatemala
data_gt = {
    'categoria': [
        'WASH', 'WASH',
        'Protección Niñez', 'Protección Niñez',
        'VBG',
        'Seguridad Alimentaria', 'Seguridad Alimentaria', 'Seguridad Alimentaria'
    ],
    'indicador': [
        'Kits de WASH/higiene distribuidos',
        'Personas que reciben mensajes de WASH',
        'Niños/as que reciben apoyo de protección',
        'Personas en espacios amigables',
        'Staff de socios capacitados',
        'Transferencias monetarias GLOBAL',
        'Transferencias monetarias CASH',
        'Valor total transferencias USD'
    ],
    'unidad': ['Kits', 'Personas', 'Niños', 'Personas', 'Personas', 'Personas', 'Personas', 'USD'],
    'meta': [3600, 18000, 180, 3000, 100, 10000, 10000, 900000],
    'logro': [2800, 14500, 135, 2400, 78, 8200, 7800, 680000],
    'peso': [29, 29, 10, 10, 3, 58, 58, 58]
}

# ES - El Salvador
data_es = {
    'categoria': [
        'WASH', 'WASH', 'WASH', 'WASH',
        'Protección', 'Protección', 'Protección',
        'VBG',
        'Protección Niñez', 'Protección Niñez', 'Protección Niñez', 'Protección Niñez',
        'Seguridad Alimentaria', 'Seguridad Alimentaria', 'Seguridad Alimentaria', 
        'Seguridad Alimentaria', 'Seguridad Alimentaria', 'Seguridad Alimentaria'
    ],
    'indicador': [
        'Hogares con kits de higiene',
        'Personas con mensajes WASH',
        'Personas con agua segura',
        '% mecanismo de quejas',
        'Asistencia legal/asesoría',
        'Apoyo psicosocial por violencia',
        '% mecanismo de quejas',
        'Prevención/mitigación de violencia',
        'Niños/as apoyo protección',
        'Personas en espacios amigables',
        'Transferencias efectivo niñez',
        'Valor transferencias niñez USD',
        'Transferencia multipropósito',
        'Valor cash multipropósito USD',
        'Transferencias recurrentes',
        '% consultados respuesta',
        'Insumos agrícolas',
        'Kits de pesca'
    ],
    'unidad': ['Hogares', 'Personas', 'Personas', '%', 'Personas', 'Personas', '%', 'Personas', 
               'Niños', 'Personas', 'Personas', 'USD', 'Personas', 'USD', 'Personas', '%', 'Personas', 'Personas'],
    'meta': [11892, 25625, 12800, 55, 331, 991, 55, 3499, 418, 1930, 251, 37650, 14677, 1682640, 14677, 55, 3929, 613],
    'logro': [8500, 18500, 9200, 42, 230, 720, 42, 2600, 310, 1450, 185, 27500, 10500, 1200000, 10500, 42, 2800, 440],
    'peso': [25, 25, 25, 25, 4, 4, 4, 4, 11, 11, 11, 11, 56, 56, 56, 56, 56, 56]
}

# HN - Honduras (ACNUR + PMA)
data_hn_acnur = {
    'categoria': [
        'Gestión de Casos', 'Gestión de Casos',
        'SMAPS',
        'Entrega de Kits',
        'Fortalecimiento Liderazgo'
    ],
    'indicador': [
        'Niños/as gestión de casos',
        'Familiares gestión de casos',
        'Personas SMAPS',
        'Kits higiene/dignidad',
        'Líderes comunitarios fortalecidos'
    ],
    'unidad': ['Niños', 'Personas', 'Personas', 'Personas', 'Personas'],
    'meta': [180, 360, 6033, 3010, 131],
    'logro': [145, 295, 5100, 2550, 108],
    'programa': ['ACNUR'] * 5,
    'peso': [0, 0, 0, 0, 0]
}

data_hn_pma = {
    'categoria': [
        'Objetivo 1', 'Objetivo 1', 'Objetivo 1',
        'Objetivo 2', 'Objetivo 2', 'Objetivo 2',
        'Objetivo 3'
    ],
    'indicador': [
        'Sensibilización - Total',
        'Sensibilización - Ocotepeque',
        'Sensibilización - Santa Bárbara',
        'Acompañamiento - Total',
        'Acompañamiento - Ocotepeque',
        'Acompañamiento - Santa Bárbara',
        'Monitoreo y sistematización'
    ],
    'unidad': ['Hogares', 'Hogares', 'Hogares', 'Hogares', 'Hogares', 'Hogares', 'Informe'],
    'meta': [3665, 1500, 2165, 3665, 1500, 2165, 1],
    'logro': [2850, 1200, 1650, 2750, 1150, 1600, 0.5],
    'programa': ['PMA'] * 7,
    'peso': [0, 0, 0, 0, 0, 0, 0]
}

data_hn_combinado = {
    'categoria': data_hn_acnur['categoria'] + data_hn_pma['categoria'],
    'indicador': data_hn_acnur['indicador'] + data_hn_pma['indicador'],
    'unidad': data_hn_acnur['unidad'] + data_hn_pma['unidad'],
    'meta': data_hn_acnur['meta'] + data_hn_pma['meta'],
    'logro': data_hn_acnur['logro'] + data_hn_pma['logro'],
    'programa': data_hn_acnur['programa'] + data_hn_pma['programa'],
    'peso': data_hn_acnur['peso'] + data_hn_pma['peso']
}

data_hn = data_hn_combinado

# ============ DATOS DE MUNICIPIOS (para el mapa) ============
municipios_data = [
    # GT
    {'pais': 'Guatemala', 'departamento': 'Alta Verapaz', 'municipio': 'Santa Catalina La Tinta', 'lat': 15.5975, 'lon': -89.8857, 'cumplimiento': 82, 'programa': 'GT'},
    {'pais': 'Guatemala', 'departamento': 'Alta Verapaz', 'municipio': 'Panzós (Telemán)', 'lat': 15.4000, 'lon': -89.6667, 'cumplimiento': 68, 'programa': 'GT'},
    {'pais': 'Guatemala', 'departamento': 'Quiché', 'municipio': 'San Antonio Ilotenango', 'lat': 15.0497, 'lon': -91.2670, 'cumplimiento': 85, 'programa': 'GT'},
    {'pais': 'Guatemala', 'departamento': 'Quiché', 'municipio': 'Joyabaj', 'lat': 14.9928, 'lon': -90.8000, 'cumplimiento': 72, 'programa': 'GT'},
    {'pais': 'Guatemala', 'departamento': 'Quiché', 'municipio': 'Canillá', 'lat': 15.1467, 'lon': -91.3158, 'cumplimiento': 88, 'programa': 'GT'},
    # ES
    {'pais': 'El Salvador', 'departamento': 'Santa Ana', 'municipio': 'Santa Ana Este', 'lat': 14.0167, 'lon': -89.4333, 'cumplimiento': 75, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'Santa Ana', 'municipio': 'Santa Ana Centro', 'lat': 14.0200, 'lon': -89.4400, 'cumplimiento': 78, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'Ahuachapán', 'municipio': 'Ahuachapán Sur', 'lat': 13.9333, 'lon': -89.8500, 'cumplimiento': 70, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'Chalatenango', 'municipio': 'Chalatenango Centro', 'lat': 14.0333, 'lon': -89.0500, 'cumplimiento': 68, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'La Unión', 'municipio': 'La Unión Norte', 'lat': 13.5000, 'lon': -87.8667, 'cumplimiento': 65, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'La Libertad', 'municipio': 'La Libertad Centro', 'lat': 13.6833, 'lon': -89.2833, 'cumplimiento': 74, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'La Libertad', 'municipio': 'La Libertad Costa', 'lat': 13.6900, 'lon': -89.2900, 'cumplimiento': 72, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'La Libertad', 'municipio': 'La Libertad Oeste', 'lat': 13.7000, 'lon': -89.3000, 'cumplimiento': 70, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'Morazán', 'municipio': 'Morazán Sur', 'lat': 13.7667, 'lon': -88.1000, 'cumplimiento': 68, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'San Miguel', 'municipio': 'San Miguel Centro', 'lat': 13.4833, 'lon': -88.1833, 'cumplimiento': 76, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'San Salvador', 'municipio': 'San Salvador Este', 'lat': 13.7000, 'lon': -89.1900, 'cumplimiento': 80, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'San Salvador', 'municipio': 'San Salvador Oeste', 'lat': 13.7000, 'lon': -89.2100, 'cumplimiento': 78, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'San Salvador', 'municipio': 'San Salvador Sur', 'lat': 13.6900, 'lon': -89.2000, 'cumplimiento': 75, 'programa': 'ES'},
    {'pais': 'El Salvador', 'departamento': 'Usulután', 'municipio': 'Usulután Este', 'lat': 13.4167, 'lon': -88.4667, 'cumplimiento': 69, 'programa': 'ES'},
    # HN - ACNUR
    {'pais': 'Honduras', 'departamento': 'Santa Bárbara', 'municipio': 'Santa Bárbara', 'lat': 15.4667, 'lon': -88.3667, 'cumplimiento': 85, 'programa': 'ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Santa Bárbara', 'municipio': 'Quimistán', 'lat': 15.3500, 'lon': -88.4000, 'cumplimiento': 82, 'programa': 'ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Cortés', 'municipio': 'San Pedro Sula', 'lat': 15.5000, 'lon': -88.0333, 'cumplimiento': 88, 'programa': 'ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Francisco Morazán', 'municipio': 'Villa Nueva', 'lat': 14.0333, 'lon': -87.0833, 'cumplimiento': 80, 'programa': 'ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Francisco Morazán', 'municipio': 'Tegucigalpa', 'lat': 14.0833, 'lon': -87.2167, 'cumplimiento': 86, 'programa': 'ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Ocotepeque', 'municipio': 'Ocotepeque', 'lat': 14.4333, 'lon': -89.2000, 'cumplimiento': 78, 'programa': 'ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Comayagua', 'municipio': 'Comayagua', 'lat': 14.4500, 'lon': -87.6333, 'cumplimiento': 84, 'programa': 'ACNUR'},
    # HN - PMA
    {'pais': 'Honduras', 'departamento': 'Santa Bárbara', 'municipio': 'Santa Bárbara (PMA)', 'lat': 15.4750, 'lon': -88.3750, 'cumplimiento': 76, 'programa': 'PMA'},
    {'pais': 'Honduras', 'departamento': 'Santa Bárbara', 'municipio': 'Quimistán (PMA)', 'lat': 15.3580, 'lon': -88.4080, 'cumplimiento': 76, 'programa': 'PMA'},
    {'pais': 'Honduras', 'departamento': 'Ocotepeque', 'municipio': 'Ocotepeque (PMA)', 'lat': 14.4400, 'lon': -89.2100, 'cumplimiento': 79, 'programa': 'PMA'}
]

df_municipios = pd.DataFrame(municipios_data)

# ============ FUNCIONES ============
def get_estado(pct):
    if pct >= 85:
        return '🟢'
    elif pct >= 60:
        return '🟡'
    else:
        return '🔴'

def procesar_data(data, proyecto):
    df = pd.DataFrame(data)
    df['% Cumplimiento'] = (df['logro'] / df['meta'] * 100).round(1)
    df['Estado'] = df['% Cumplimiento'].apply(get_estado)
    df['Proyecto'] = proyecto
    return df

df_gt = procesar_data(data_gt, 'Guatemala')
df_es = procesar_data(data_es, 'El Salvador')
df_hn = procesar_data(data_hn, 'Honduras')

# ============ FUNCIONES DE VISUALIZACIÓN ============

def mostrar_tabla_indicadores(df, proyecto, programa_filtro=None):
    df_display = df.copy()
    if programa_filtro and 'programa' in df_display.columns and programa_filtro != 'Todos':
        df_display = df_display[df_display['programa'] == programa_filtro]
    
    columnas = ['categoria', 'indicador', 'unidad', 'meta', 'logro', '% Cumplimiento', 'Estado']
    if 'programa' in df_display.columns:
        columnas.insert(1, 'programa')
    
    st.dataframe(
        df_display[columnas],
        use_container_width=True,
        hide_index=True,
        column_config={
            'categoria': 'Categoría',
            'programa': 'Programa',
            'indicador': 'Indicador',
            'unidad': 'Unidad',
            'meta': st.column_config.NumberColumn('Meta', format="%d"),
            'logro': st.column_config.NumberColumn('Logro', format="%d"),
            '% Cumplimiento': st.column_config.NumberColumn('%', format="%.1f"),
            'Estado': 'Estado'
        }
    )

def mostrar_alertas(df, programa_filtro=None):
    df_alerts = df.copy()
    if programa_filtro and 'programa' in df_alerts.columns and programa_filtro != 'Todos':
        df_alerts = df_alerts[df_alerts['programa'] == programa_filtro]
    
    alertas = df_alerts[df_alerts['Estado'] != '🟢']
    if len(alertas) > 0:
        for _, row in alertas.iterrows():
            if row['Estado'] == '🔴':
                st.error(f"🔴 **CRÍTICO**: {row['indicador']} - {row['% Cumplimiento']}% ({row['logro']:.1f}/{row['meta']:.0f} {row['unidad']})")
            else:
                st.warning(f"🟡 **ATENCIÓN**: {row['indicador']} - {row['% Cumplimiento']}% ({row['logro']:.1f}/{row['meta']:.0f} {row['unidad']})")
    else:
        st.success("✅ ¡Todos los indicadores están en verde!")

# ============ INTERFAZ PRINCIPAL ============

st.title("🌍 Monitoreo Humanitario - Centroamérica")

# ============ SIDEBAR ============
with st.sidebar:
    st.header("🎯 Filtros")
    
    pais_filtro = st.selectbox("🌍 País", options=['Todos', 'Guatemala', 'El Salvador', 'Honduras'], index=0)
    
    if pais_filtro == 'Honduras' or pais_filtro == 'Todos':
        programa_options = ['Todos', 'ACNUR', 'PMA']
    else:
        programa_options = ['Todos']
    
    programa_filtro = st.selectbox("📂 Programa", options=programa_options, index=0)
    
    st.markdown("---")
    st.header("📊 Resumen Global")
    
    gt_global = (df_gt['logro'].sum() / df_gt['meta'].sum() * 100)
    es_global = (df_es['logro'].sum() / df_es['meta'].sum() * 100)
    
    df_hn_acnur = df_hn[df_hn['programa'] == 'ACNUR']
    hn_acnur_global = (df_hn_acnur['logro'].sum() / df_hn_acnur['meta'].sum() * 100) if len(df_hn_acnur) > 0 else 0
    
    df_hn_pma = df_hn[df_hn['programa'] == 'PMA']
    hn_pma_global = (df_hn_pma['logro'].sum() / df_hn_pma['meta'].sum() * 100) if len(df_hn_pma) > 0 else 0
    
    st.metric("🇬🇹 Guatemala", f"{gt_global:.1f}%")
    st.metric("🇸🇻 El Salvador", f"{es_global:.1f}%")
    st.metric("🇭🇳 HN - ACNUR", f"{hn_acnur_global:.1f}%")
    st.metric("🇭🇳 HN - PMA", f"{hn_pma_global:.1f}%")

# ============ MAPA CON ST.MAP() ============
st.subheader("🗺️ Mapa de Intervención")

# Filtrar datos para el mapa
df_mapa = df_municipios.copy()
if pais_filtro != 'Todos':
    df_mapa = df_mapa[df_mapa['pais'] == pais_filtro]
if programa_filtro != 'Todos':
    df_mapa = df_mapa[df_mapa['programa'] == programa_filtro]

# Crear mapa con st.map()
if len(df_mapa) > 0:
    # Preparar datos para el mapa
    mapa_data = df_mapa[['lat', 'lon']].copy()
    mapa_data['size'] = df_mapa['cumplimiento'] / 10  # Tamaño proporcional
    
    # Mostrar mapa
    st.map(mapa_data, size='size', zoom=6, use_container_width=True)
    
    # Mostrar tabla de municipios
    st.dataframe(
        df_mapa[['municipio', 'departamento', 'pais', 'programa', 'cumplimiento']],
        use_container_width=True,
        hide_index=True,
        column_config={
            'municipio': 'Municipio',
            'departamento': 'Departamento',
            'pais': 'País',
            'programa': 'Programa',
            'cumplimiento': st.column_config.NumberColumn('Cumplimiento %', format="%.0f%%")
        }
    )
else:
    st.info("No hay municipios para mostrar con los filtros seleccionados.")

# ============ DETALLE DE PROYECTOS ============
st.markdown("---")
st.subheader("📊 Datos de Proyectos por País")

tab1, tab2, tab3 = st.tabs(["🇬🇹 Guatemala", "🇸🇻 El Salvador", "🇭🇳 Honduras"])

with tab1:
    st.header("🇬🇹 Guatemala")
    st.caption("Período: Mayo - Noviembre 2026")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pct = df_gt[df_gt['categoria']=='WASH']['% Cumplimiento'].mean()
        st.metric("WASH (29%)", f"{pct:.0f}%")
    with col2:
        pct = df_gt[df_gt['categoria']=='Protección Niñez']['% Cumplimiento'].mean()
        st.metric("Niñez (10%)", f"{pct:.0f}%")
    with col3:
        pct = df_gt[df_gt['categoria']=='VBG']['% Cumplimiento'].mean()
        st.metric("VBG (3%)", f"{pct:.0f}%")
    with col4:
        pct = df_gt[df_gt['categoria']=='Seguridad Alimentaria']['% Cumplimiento'].mean()
        st.metric("Seg. Alim (58%)", f"{pct:.0f}%")
    
    mostrar_tabla_indicadores(df_gt, 'Guatemala')
    mostrar_alertas(df_gt)

with tab2:
    st.header("🇸🇻 El Salvador")
    st.caption("Período: Mayo - Noviembre 2026")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        pct = df_es[df_es['categoria']=='WASH']['% Cumplimiento'].mean()
        st.metric("WASH (25%)", f"{pct:.0f}%")
    with col2:
        pct = df_es[df_es['categoria']=='Protección']['% Cumplimiento'].mean()
        st.metric("Protección (4%)", f"{pct:.0f}%")
    with col3:
        pct = df_es[df_es['categoria']=='VBG']['% Cumplimiento'].mean()
        st.metric("VBG (4%)", f"{pct:.0f}%")
    with col4:
        pct = df_es[df_es['categoria']=='Protección Niñez']['% Cumplimiento'].mean()
        st.metric("Niñez (11%)", f"{pct:.0f}%")
    with col5:
        pct = df_es[df_es['categoria']=='Seguridad Alimentaria']['% Cumplimiento'].mean()
        st.metric("Seg. Alim (56%)", f"{pct:.0f}%")
    
    mostrar_tabla_indicadores(df_es, 'El Salvador')
    mostrar_alertas(df_es)

with tab3:
    st.header("🇭🇳 Honduras")
    st.caption("Período: Mayo - Octubre 2026")
    
    hn_programa = st.radio("📂 Seleccionar Programa", options=['Todos', 'ACNUR', 'PMA'], horizontal=True)
    
    if hn_programa == 'ACNUR' or hn_programa == 'Todos':
        st.subheader("🔵 ACNUR")
        df_hn_acnur = df_hn[df_hn['programa'] == 'ACNUR']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            pct = df_hn_acnur[df_hn_acnur['categoria']=='Gestión de Casos']['% Cumplimiento'].mean()
            st.metric("Gestión Casos", f"{pct:.0f}%")
        with col2:
            pct = df_hn_acnur[df_hn_acnur['categoria']=='SMAPS']['% Cumplimiento'].mean()
            st.metric("SMAPS", f"{pct:.0f}%")
        with col3:
            pct = df_hn_acnur[df_hn_acnur['categoria']=='Entrega de Kits']['% Cumplimiento'].mean()
            st.metric("Kits", f"{pct:.0f}%")
        with col4:
            pct = df_hn_acnur[df_hn_acnur['categoria']=='Fortalecimiento Liderazgo']['% Cumplimiento'].mean()
            st.metric("Liderazgo", f"{pct:.0f}%")
        
        mostrar_tabla_indicadores(df_hn_acnur, 'Honduras', 'ACNUR')
        mostrar_alertas(df_hn_acnur, 'ACNUR')
        st.markdown("---")
    
    if hn_programa == 'PMA' or hn_programa == 'Todos':
        st.subheader("🟢 PMA")
        df_hn_pma = df_hn[df_hn['programa'] == 'PMA']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pct = df_hn_pma[df_hn_pma['categoria']=='Objetivo 1']['% Cumplimiento'].mean()
            st.metric("Objetivo 1 (Sensibilización)", f"{pct:.0f}%")
        with col2:
            pct = df_hn_pma[df_hn_pma['categoria']=='Objetivo 2']['% Cumplimiento'].mean()
            st.metric("Objetivo 2 (Acompañamiento)", f"{pct:.0f}%")
        with col3:
            pct = df_hn_pma[df_hn_pma['categoria']=='Objetivo 3']['% Cumplimiento'].mean()
            st.metric("Objetivo 3 (Monitoreo)", f"{pct:.0f}%")
        
        mostrar_tabla_indicadores(df_hn_pma, 'Honduras', 'PMA')
        mostrar_alertas(df_hn_pma, 'PMA')

# ============ FOOTER ============
st.markdown("---")
st.caption("📅 Datos simulados - Última actualización: 30 de julio 2026")
st.caption("💡 GT y ES: Mayo - Noviembre 2026 | HN: Mayo - Octubre 2026")
