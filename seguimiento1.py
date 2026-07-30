import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date

# ============ CONFIGURACIÓN ============
st.set_page_config(
    page_title="Monitoreo Humanitario - Centroamérica",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ DATOS DE LOS PROYECTOS ============

# GT - Guatemala (🔵 Azul)
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
    'peso': [29, 29, 10, 10, 3, 58, 58, 58],
    'programa': ['🔵 GT'] * 8
}

# ES - El Salvador (🔷 Azul oscuro)
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
    'peso': [25, 25, 25, 25, 4, 4, 4, 4, 11, 11, 11, 11, 56, 56, 56, 56, 56, 56],
    'programa': ['🔷 ES'] * 18
}

# HN - Honduras ACNUR (🔹 Celeste)
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
    'programa': ['🔹 ACNUR'] * 5,
    'peso': [0, 0, 0, 0, 0]
}

# HN - Honduras PMA (🟢 Verde)
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
    'programa': ['🟢 PMA'] * 7,
    'peso': [0, 0, 0, 0, 0, 0, 0]
}

# Combinar HN
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

# ============ DATOS DE MUNICIPIOS CON DISTINCIÓN VISUAL ============
municipios_data = [
    # GT - 🔵 Azul
    {'pais': 'Guatemala', 'departamento': 'Alta Verapaz', 'municipio': '🔵 Santa Catalina La Tinta', 'lat': 15.5975, 'lon': -89.8857, 'cumplimiento': 82, 'programa': '🔵 GT'},
    {'pais': 'Guatemala', 'departamento': 'Alta Verapaz', 'municipio': '🔵 Panzós (Telemán)', 'lat': 15.4000, 'lon': -89.6667, 'cumplimiento': 68, 'programa': '🔵 GT'},
    {'pais': 'Guatemala', 'departamento': 'Quiché', 'municipio': '🔵 San Antonio Ilotenango', 'lat': 15.0497, 'lon': -91.2670, 'cumplimiento': 85, 'programa': '🔵 GT'},
    {'pais': 'Guatemala', 'departamento': 'Quiché', 'municipio': '🔵 Joyabaj', 'lat': 14.9928, 'lon': -90.8000, 'cumplimiento': 72, 'programa': '🔵 GT'},
    {'pais': 'Guatemala', 'departamento': 'Quiché', 'municipio': '🔵 Canillá', 'lat': 15.1467, 'lon': -91.3158, 'cumplimiento': 88, 'programa': '🔵 GT'},
    
    # ES - 🔷 Azul oscuro
    {'pais': 'El Salvador', 'departamento': 'Santa Ana', 'municipio': '🔷 Santa Ana Este', 'lat': 14.0167, 'lon': -89.4333, 'cumplimiento': 75, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'Santa Ana', 'municipio': '🔷 Santa Ana Centro', 'lat': 14.0200, 'lon': -89.4400, 'cumplimiento': 78, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'Ahuachapán', 'municipio': '🔷 Ahuachapán Sur', 'lat': 13.9333, 'lon': -89.8500, 'cumplimiento': 70, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'Chalatenango', 'municipio': '🔷 Chalatenango Centro', 'lat': 14.0333, 'lon': -89.0500, 'cumplimiento': 68, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'La Unión', 'municipio': '🔷 La Unión Norte', 'lat': 13.5000, 'lon': -87.8667, 'cumplimiento': 65, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'La Libertad', 'municipio': '🔷 La Libertad Centro', 'lat': 13.6833, 'lon': -89.2833, 'cumplimiento': 74, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'La Libertad', 'municipio': '🔷 La Libertad Costa', 'lat': 13.6900, 'lon': -89.2900, 'cumplimiento': 72, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'La Libertad', 'municipio': '🔷 La Libertad Oeste', 'lat': 13.7000, 'lon': -89.3000, 'cumplimiento': 70, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'Morazán', 'municipio': '🔷 Morazán Sur', 'lat': 13.7667, 'lon': -88.1000, 'cumplimiento': 68, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'San Miguel', 'municipio': '🔷 San Miguel Centro', 'lat': 13.4833, 'lon': -88.1833, 'cumplimiento': 76, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'San Salvador', 'municipio': '🔷 San Salvador Este', 'lat': 13.7000, 'lon': -89.1900, 'cumplimiento': 80, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'San Salvador', 'municipio': '🔷 San Salvador Oeste', 'lat': 13.7000, 'lon': -89.2100, 'cumplimiento': 78, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'San Salvador', 'municipio': '🔷 San Salvador Sur', 'lat': 13.6900, 'lon': -89.2000, 'cumplimiento': 75, 'programa': '🔷 ES'},
    {'pais': 'El Salvador', 'departamento': 'Usulután', 'municipio': '🔷 Usulután Este', 'lat': 13.4167, 'lon': -88.4667, 'cumplimiento': 69, 'programa': '🔷 ES'},
    
    # HN - ACNUR (🔹 Celeste)
    {'pais': 'Honduras', 'departamento': 'Santa Bárbara', 'municipio': '🔹 Santa Bárbara', 'lat': 15.4667, 'lon': -88.3667, 'cumplimiento': 85, 'programa': '🔹 ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Santa Bárbara', 'municipio': '🔹 Quimistán', 'lat': 15.3500, 'lon': -88.4000, 'cumplimiento': 82, 'programa': '🔹 ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Cortés', 'municipio': '🔹 San Pedro Sula', 'lat': 15.5000, 'lon': -88.0333, 'cumplimiento': 88, 'programa': '🔹 ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Francisco Morazán', 'municipio': '🔹 Villa Nueva', 'lat': 14.0333, 'lon': -87.0833, 'cumplimiento': 80, 'programa': '🔹 ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Francisco Morazán', 'municipio': '🔹 Tegucigalpa', 'lat': 14.0833, 'lon': -87.2167, 'cumplimiento': 86, 'programa': '🔹 ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Ocotepeque', 'municipio': '🔹 Ocotepeque', 'lat': 14.4333, 'lon': -89.2000, 'cumplimiento': 78, 'programa': '🔹 ACNUR'},
    {'pais': 'Honduras', 'departamento': 'Comayagua', 'municipio': '🔹 Comayagua', 'lat': 14.4500, 'lon': -87.6333, 'cumplimiento': 84, 'programa': '🔹 ACNUR'},
    
    # HN - PMA (🟢 Verde)
    {'pais': 'Honduras', 'departamento': 'Santa Bárbara', 'municipio': '🟢 Santa Bárbara (PMA)', 'lat': 15.4750, 'lon': -88.3750, 'cumplimiento': 76, 'programa': '🟢 PMA'},
    {'pais': 'Honduras', 'departamento': 'Santa Bárbara', 'municipio': '🟢 Quimistán (PMA)', 'lat': 15.3580, 'lon': -88.4080, 'cumplimiento': 76, 'programa': '🟢 PMA'},
    {'pais': 'Honduras', 'departamento': 'Ocotepeque', 'municipio': '🟢 Ocotepeque (PMA)', 'lat': 14.4400, 'lon': -89.2100, 'cumplimiento': 79, 'programa': '🟢 PMA'}
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

def mostrar_tabla_indicadores(df, programa_filtro=None):
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

# ============ FUNCIÓN RESÚMEN EJECUTIVO ============

def mostrar_resumen_ejecutivo():
    """Muestra el resumen ejecutivo con cronograma, finanzas y metas"""
    
    st.header("📊 Resumen Ejecutivo")
    
    # ===== 1. CRONOGRAMA DEL PROGRAMA =====
    st.subheader("📋 Cronograma del Programa")
    
    # Fechas de los proyectos
    fechas = {
        '🔵 GT': {'inicio': date(2026, 5, 1), 'fin': date(2026, 11, 30)},
        '🔷 ES': {'inicio': date(2026, 5, 1), 'fin': date(2026, 11, 30)},
        '🔹 ACNUR': {'inicio': date(2026, 5, 1), 'fin': date(2026, 10, 31)},
        '🟢 PMA': {'inicio': date(2026, 5, 1), 'fin': date(2026, 10, 31)}
    }
    
    hoy = date(2026, 7, 30)  # Fecha actual simulada
    
    cronograma_data = []
    for programa, fechas_prog in fechas.items():
        total_dias = (fechas_prog['fin'] - fechas_prog['inicio']).days
        dias_transcurridos = (hoy - fechas_prog['inicio']).days
        if dias_transcurridos < 0:
            pct = 0
        elif dias_transcurridos > total_dias:
            pct = 100
        else:
            pct = (dias_transcurridos / total_dias * 100)
        cronograma_data.append({
            'Programa': programa,
            '% Tiempo': round(pct, 1),
            'Inicio': fechas_prog['inicio'].strftime('%d/%m/%Y'),
            'Fin': fechas_prog['fin'].strftime('%d/%m/%Y'),
            'Días': f"{dias_transcurridos}/{total_dias}"
        })
    
    df_cronograma = pd.DataFrame(cronograma_data)
    
    # Mostrar barras de progreso
    cols = st.columns(len(df_cronograma))
    for idx, (col, row) in enumerate(zip(cols, df_cronograma.iterrows())):
        with col:
            _, row_data = row
            prog = row_data['% Tiempo']
            st.metric(
                label=f"{row_data['Programa']}",
                value=f"{prog:.0f}%",
                delta=f"{row_data['Días']} días"
            )
            st.progress(prog/100)
            st.caption(f"{row_data['Inicio']} → {row_data['Fin']}")
    
    st.markdown("---")
    
    # ===== 2. AVANCE FINANCIERO =====
    st.subheader("💰 Avance Financiero")
    
    # Datos financieros simulados
    finanzas_data = [
        {'Programa': '🔵 GT', 'Presupuesto': 4000000, 'Ejecutado': 2800000},
        {'Programa': '🔷 ES', 'Presupuesto': 5000000, 'Ejecutado': 3200000},
        {'Programa': '🔹 ACNUR', 'Presupuesto': 1000000, 'Ejecutado': 700000},
        {'Programa': '🟢 PMA', 'Presupuesto': 1000000, 'Ejecutado': 600000}
    ]
    
    df_finanzas = pd.DataFrame(finanzas_data)
    df_finanzas['% Ejecución'] = (df_finanzas['Ejecutado'] / df_finanzas['Presupuesto'] * 100).round(1)
    df_finanzas['Estado'] = df_finanzas['% Ejecución'].apply(get_estado)
    
    # Formatear como moneda
    df_finanzas['Presupuesto'] = df_finanzas['Presupuesto'].apply(lambda x: f"${x/1000000:.1f}M")
    df_finanzas['Ejecutado'] = df_finanzas['Ejecutado'].apply(lambda x: f"${x/1000000:.1f}M")
    
    st.dataframe(
        df_finanzas[['Programa', 'Presupuesto', 'Ejecutado', '% Ejecución', 'Estado']],
        use_container_width=True,
        hide_index=True,
        column_config={
            'Programa': 'Programa',
            'Presupuesto': 'Presupuesto',
            'Ejecutado': 'Ejecutado',
            '% Ejecución': st.column_config.NumberColumn('% Ejecución', format="%.1f%%"),
            'Estado': 'Estado'
        }
    )
    
    # Gráfico de barras financiero (usando st.bar_chart)
    st.caption("📊 Comparativa de Ejecución Financiera")
    chart_data = df_finanzas.copy()
    chart_data['% Ejecución'] = chart_data['% Ejecución'].astype(float)
    st.bar_chart(chart_data.set_index('Programa')['% Ejecución'], height=250)
    
    st.markdown("---")
    
    # ===== 3. AVANCE DE METAS =====
    st.subheader("🎯 Avance de Metas")
    
    # Calcular cumplimiento por programa
    gt_pct = (df_gt['logro'].sum() / df_gt['meta'].sum() * 100)
    es_pct = (df_es['logro'].sum() / df_es['meta'].sum() * 100)
    
    df_hn_acnur = df_hn[df_hn['programa'] == '🔹 ACNUR']
    hn_acnur_pct = (df_hn_acnur['logro'].sum() / df_hn_acnur['meta'].sum() * 100) if len(df_hn_acnur) > 0 else 0
    
    df_hn_pma = df_hn[df_hn['programa'] == '🟢 PMA']
    hn_pma_pct = (df_hn_pma['logro'].sum() / df_hn_pma['meta'].sum() * 100) if len(df_hn_pma) > 0 else 0
    
    metas_data = [
        {'Programa': '🔵 GT', 'Cumplimiento': gt_pct, 'Estado': get_estado(gt_pct)},
        {'Programa': '🔷 ES', 'Cumplimiento': es_pct, 'Estado': get_estado(es_pct)},
        {'Programa': '🔹 ACNUR', 'Cumplimiento': hn_acnur_pct, 'Estado': get_estado(hn_acnur_pct)},
        {'Programa': '🟢 PMA', 'Cumplimiento': hn_pma_pct, 'Estado': get_estado(hn_pma_pct)}
    ]
    
    df_metas = pd.DataFrame(metas_data)
    df_metas['Cumplimiento'] = df_metas['Cumplimiento'].round(1)
    
    # Mostrar tarjetas de cumplimiento
    cols = st.columns(len(df_metas))
    for idx, (col, row) in enumerate(zip(cols, df_metas.iterrows())):
        with col:
            _, row_data = row
            st.metric(
                label=f"{row_data['Programa']}",
                value=f"{row_data['Cumplimiento']:.0f}%",
                delta=row_data['Estado']
            )
    
    # Gráfico de barras de cumplimiento
    st.caption("📊 Comparativa de Cumplimiento de Metas")
    chart_data2 = df_metas.copy()
    chart_data2['Cumplimiento'] = chart_data2['Cumplimiento'].astype(float)
    st.bar_chart(chart_data2.set_index('Programa')['Cumplimiento'], height=250, color='#1a5276')

# ============ INTERFAZ PRINCIPAL ============

st.title("🌍 Monitoreo Humanitario - Centroamérica")

# ============ SIDEBAR ============
with st.sidebar:
    st.header("🎯 Filtros")
    
    pais_filtro = st.selectbox("🌍 País", options=['Todos', 'Guatemala', 'El Salvador', 'Honduras'], index=0)
    
    # FILTRO DE PROGRAMA SOLO PARA HONDURAS
    if pais_filtro == 'Honduras':
        programa_options = ['Todos', '🔹 ACNUR', '🟢 PMA']
        programa_filtro = st.selectbox("📂 Programa", options=programa_options, index=0)
        st.caption("🔹 ACNUR | 🟢 PMA")
    else:
        programa_filtro = 'Todos'
        if pais_filtro == 'Todos':
            st.info("💡 Selecciona 'Honduras' para filtrar por programa")
    
    st.markdown("---")
    st.header("📊 Resumen Global")
    
    gt_global = (df_gt['logro'].sum() / df_gt['meta'].sum() * 100)
    es_global = (df_es['logro'].sum() / df_es['meta'].sum() * 100)
    
    df_hn_acnur = df_hn[df_hn['programa'] == '🔹 ACNUR']
    hn_acnur_global = (df_hn_acnur['logro'].sum() / df_hn_acnur['meta'].sum() * 100) if len(df_hn_acnur) > 0 else 0
    
    df_hn_pma = df_hn[df_hn['programa'] == '🟢 PMA']
    hn_pma_global = (df_hn_pma['logro'].sum() / df_hn_pma['meta'].sum() * 100) if len(df_hn_pma) > 0 else 0
    
    st.metric("🔵 Guatemala", f"{gt_global:.1f}%")
    st.metric("🔷 El Salvador", f"{es_global:.1f}%")
    st.metric("🔹 HN - ACNUR", f"{hn_acnur_global:.1f}%")
    st.metric("🟢 HN - PMA", f"{hn_pma_global:.1f}%")

# ============ PESTAÑAS ============
tab_resumen, tab_mapa, tab_gt, tab_es, tab_hn = st.tabs([
    "📊 Resumen Ejecutivo",
    "🗺️ Mapa",
    "🔵 Guatemala",
    "🔷 El Salvador",
    "🇭🇳 Honduras"
])

with tab_resumen:
    mostrar_resumen_ejecutivo()

with tab_mapa:
    st.header("🗺️ Mapa de Intervención")
    
    # Filtrar datos para el mapa
    df_mapa = df_municipios.copy()
    if pais_filtro != 'Todos':
        df_mapa = df_mapa[df_mapa['pais'] == pais_filtro]
    if programa_filtro != 'Todos' and pais_filtro == 'Honduras':
        df_mapa = df_mapa[df_mapa['programa'] == programa_filtro]
    
    if len(df_mapa) > 0:
        st.map(df_mapa[['lat', 'lon']], zoom=6, use_container_width=True)
        st.caption("🔵 GT | 🔷 ES | 🔹 ACNUR | 🟢 PMA")
        
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

with tab_gt:
    st.header("🔵 Guatemala")
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
    
    mostrar_tabla_indicadores(df_gt)
    mostrar_alertas(df_gt)

with tab_es:
    st.header("🔷 El Salvador")
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
    
    mostrar_tabla_indicadores(df_es)
    mostrar_alertas(df_es)

with tab_hn:
    st.header("🇭🇳 Honduras")
    st.caption("Período: Mayo - Octubre 2026")
    
    hn_programa = st.radio("📂 Seleccionar Programa", options=['Todos', '🔹 ACNUR', '🟢 PMA'], horizontal=True)
    
    if hn_programa == '🔹 ACNUR' or hn_programa == 'Todos':
        st.subheader("🔹 ACNUR")
        df_hn_acnur = df_hn[df_hn['programa'] == '🔹 ACNUR']
        
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
        
        mostrar_tabla_indicadores(df_hn_acnur, '🔹 ACNUR')
        mostrar_alertas(df_hn_acnur, '🔹 ACNUR')
        st.markdown("---")
    
    if hn_programa == '🟢 PMA' or hn_programa == 'Todos':
        st.subheader("🟢 PMA")
        df_hn_pma = df_hn[df_hn['programa'] == '🟢 PMA']
        
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
        
        mostrar_tabla_indicadores(df_hn_pma, '🟢 PMA')
        mostrar_alertas(df_hn_pma, '🟢 PMA')
