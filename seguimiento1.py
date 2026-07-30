import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import folium_static
import json
import numpy as np

# ============ CONFIGURACIÓN ============
st.set_page_config(
    page_title="Monitoreo Humanitario - Centroamérica",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ ESTILOS CSS ============
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 6px solid #2ecc71;
        transition: transform 0.2s;
        margin-bottom: 15px;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    h1, h2, h3 {
        color: #2c3e50 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: white;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1a5276;
        color: white !important;
    }
    .folium-map {
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .programa-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
    }
    .acnur-badge {
        background-color: #1a5276;
        color: white;
    }
    .pma-badge {
        background-color: #27ae60;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

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

# ============ HN - HONDURAS (ACNUR + PMA) ============

# ACNUR - Datos existentes
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

# PMA - Nuevos datos
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

# ============ DATOS DE MUNICIPIOS ============

municipios_data = [
    # ===== GUATEMALA =====
    {
        'pais': 'Guatemala',
        'departamento': 'Alta Verapaz',
        'municipio': 'Santa Catalina La Tinta',
        'lat': 15.5975,
        'lon': -89.8857,
        'cumplimiento': 82,
        'estado': '🟢',
        'categorias': {'WASH': 85, 'Protección Niñez': 68, 'VBG': 75, 'Seguridad Alimentaria': 90},
        'programa': 'GT'
    },
    {
        'pais': 'Guatemala',
        'departamento': 'Alta Verapaz',
        'municipio': 'Panzós (Telemán)',
        'lat': 15.4000,
        'lon': -89.6667,
        'cumplimiento': 68,
        'estado': '🟡',
        'categorias': {'WASH': 65, 'Protección Niñez': 70, 'VBG': 72, 'Seguridad Alimentaria': 66},
        'programa': 'GT'
    },
    {
        'pais': 'Guatemala',
        'departamento': 'Quiché',
        'municipio': 'San Antonio Ilotenango',
        'lat': 15.0497,
        'lon': -91.2670,
        'cumplimiento': 85,
        'estado': '🟢',
        'categorias': {'WASH': 88, 'Protección Niñez': 82, 'VBG': 80, 'Seguridad Alimentaria': 86},
        'programa': 'GT'
    },
    {
        'pais': 'Guatemala',
        'departamento': 'Quiché',
        'municipio': 'Joyabaj',
        'lat': 14.9928,
        'lon': -90.8000,
        'cumplimiento': 72,
        'estado': '🟡',
        'categorias': {'WASH': 70, 'Protección Niñez': 68, 'VBG': 75, 'Seguridad Alimentaria': 74},
        'programa': 'GT'
    },
    {
        'pais': 'Guatemala',
        'departamento': 'Quiché',
        'municipio': 'Canillá',
        'lat': 15.1467,
        'lon': -91.3158,
        'cumplimiento': 88,
        'estado': '🟢',
        'categorias': {'WASH': 90, 'Protección Niñez': 85, 'VBG': 82, 'Seguridad Alimentaria': 89},
        'programa': 'GT'
    },
    
    # ===== EL SALVADOR =====
    {
        'pais': 'El Salvador',
        'departamento': 'Santa Ana',
        'municipio': 'Santa Ana Este',
        'lat': 14.0167,
        'lon': -89.4333,
        'cumplimiento': 75,
        'estado': '🟡',
        'categorias': {'WASH': 78, 'Protección Niñez': 72, 'VBG': 70, 'Seguridad Alimentaria': 76},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'Santa Ana',
        'municipio': 'Santa Ana Centro',
        'lat': 14.0200,
        'lon': -89.4400,
        'cumplimiento': 78,
        'estado': '🟡',
        'categorias': {'WASH': 80, 'Protección Niñez': 75, 'VBG': 74, 'Seguridad Alimentaria': 79},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'Ahuachapán',
        'municipio': 'Ahuachapán Sur',
        'lat': 13.9333,
        'lon': -89.8500,
        'cumplimiento': 70,
        'estado': '🟡',
        'categorias': {'WASH': 72, 'Protección Niñez': 68, 'VBG': 65, 'Seguridad Alimentaria': 71},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'Chalatenango',
        'municipio': 'Chalatenango Centro',
        'lat': 14.0333,
        'lon': -89.0500,
        'cumplimiento': 68,
        'estado': '🟡',
        'categorias': {'WASH': 70, 'Protección Niñez': 65, 'VBG': 62, 'Seguridad Alimentaria': 69},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'La Unión',
        'municipio': 'La Unión Norte',
        'lat': 13.5000,
        'lon': -87.8667,
        'cumplimiento': 65,
        'estado': '🟡',
        'categorias': {'WASH': 68, 'Protección Niñez': 62, 'VBG': 60, 'Seguridad Alimentaria': 66},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'La Libertad',
        'municipio': 'La Libertad Centro',
        'lat': 13.6833,
        'lon': -89.2833,
        'cumplimiento': 74,
        'estado': '🟡',
        'categorias': {'WASH': 76, 'Protección Niñez': 72, 'VBG': 70, 'Seguridad Alimentaria': 75},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'La Libertad',
        'municipio': 'La Libertad Costa',
        'lat': 13.6900,
        'lon': -89.2900,
        'cumplimiento': 72,
        'estado': '🟡',
        'categorias': {'WASH': 74, 'Protección Niñez': 70, 'VBG': 68, 'Seguridad Alimentaria': 73},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'La Libertad',
        'municipio': 'La Libertad Oeste',
        'lat': 13.7000,
        'lon': -89.3000,
        'cumplimiento': 70,
        'estado': '🟡',
        'categorias': {'WASH': 72, 'Protección Niñez': 68, 'VBG': 66, 'Seguridad Alimentaria': 71},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'Morazán',
        'municipio': 'Morazán Sur',
        'lat': 13.7667,
        'lon': -88.1000,
        'cumplimiento': 68,
        'estado': '🟡',
        'categorias': {'WASH': 70, 'Protección Niñez': 65, 'VBG': 63, 'Seguridad Alimentaria': 69},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'San Miguel',
        'municipio': 'San Miguel Centro',
        'lat': 13.4833,
        'lon': -88.1833,
        'cumplimiento': 76,
        'estado': '🟡',
        'categorias': {'WASH': 78, 'Protección Niñez': 74, 'VBG': 72, 'Seguridad Alimentaria': 77},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'San Salvador',
        'municipio': 'San Salvador Este',
        'lat': 13.7000,
        'lon': -89.1900,
        'cumplimiento': 80,
        'estado': '🟢',
        'categorias': {'WASH': 82, 'Protección Niñez': 78, 'VBG': 76, 'Seguridad Alimentaria': 81},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'San Salvador',
        'municipio': 'San Salvador Oeste',
        'lat': 13.7000,
        'lon': -89.2100,
        'cumplimiento': 78,
        'estado': '🟡',
        'categorias': {'WASH': 80, 'Protección Niñez': 76, 'VBG': 74, 'Seguridad Alimentaria': 79},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'San Salvador',
        'municipio': 'San Salvador Sur',
        'lat': 13.6900,
        'lon': -89.2000,
        'cumplimiento': 75,
        'estado': '🟡',
        'categorias': {'WASH': 77, 'Protección Niñez': 73, 'VBG': 71, 'Seguridad Alimentaria': 76},
        'programa': 'ES'
    },
    {
        'pais': 'El Salvador',
        'departamento': 'Usulután',
        'municipio': 'Usulután Este',
        'lat': 13.4167,
        'lon': -88.4667,
        'cumplimiento': 69,
        'estado': '🟡',
        'categorias': {'WASH': 71, 'Protección Niñez': 67, 'VBG': 65, 'Seguridad Alimentaria': 70},
        'programa': 'ES'
    },
    
    # ===== HONDURAS - ACNUR =====
    {
        'pais': 'Honduras',
        'departamento': 'Santa Bárbara',
        'municipio': 'Santa Bárbara',
        'lat': 15.4667,
        'lon': -88.3667,
        'cumplimiento': 85,
        'estado': '🟢',
        'categorias': {'Gestión de Casos': 84, 'SMAPS': 86, 'Entrega de Kits': 83, 'Fortalecimiento Liderazgo': 85},
        'programa': 'ACNUR'
    },
    {
        'pais': 'Honduras',
        'departamento': 'Santa Bárbara',
        'municipio': 'Quimistán',
        'lat': 15.3500,
        'lon': -88.4000,
        'cumplimiento': 82,
        'estado': '🟢',
        'categorias': {'Gestión de Casos': 80, 'SMAPS': 83, 'Entrega de Kits': 82, 'Fortalecimiento Liderazgo': 81},
        'programa': 'ACNUR'
    },
    {
        'pais': 'Honduras',
        'departamento': 'Cortés',
        'municipio': 'San Pedro Sula',
        'lat': 15.5000,
        'lon': -88.0333,
        'cumplimiento': 88,
        'estado': '🟢',
        'categorias': {'Gestión de Casos': 87, 'SMAPS': 89, 'Entrega de Kits': 86, 'Fortalecimiento Liderazgo': 88},
        'programa': 'ACNUR'
    },
    {
        'pais': 'Honduras',
        'departamento': 'Francisco Morazán',
        'municipio': 'Villa Nueva',
        'lat': 14.0333,
        'lon': -87.0833,
        'cumplimiento': 80,
        'estado': '🟢',
        'categorias': {'Gestión de Casos': 78, 'SMAPS': 81, 'Entrega de Kits': 79, 'Fortalecimiento Liderazgo': 80},
        'programa': 'ACNUR'
    },
    {
        'pais': 'Honduras',
        'departamento': 'Francisco Morazán',
        'municipio': 'Tegucigalpa',
        'lat': 14.0833,
        'lon': -87.2167,
        'cumplimiento': 86,
        'estado': '🟢',
        'categorias': {'Gestión de Casos': 85, 'SMAPS': 87, 'Entrega de Kits': 84, 'Fortalecimiento Liderazgo': 86},
        'programa': 'ACNUR'
    },
    {
        'pais': 'Honduras',
        'departamento': 'Ocotepeque',
        'municipio': 'Ocotepeque',
        'lat': 14.4333,
        'lon': -89.2000,
        'cumplimiento': 78,
        'estado': '🟡',
        'categorias': {'Gestión de Casos': 76, 'SMAPS': 79, 'Entrega de Kits': 77, 'Fortalecimiento Liderazgo': 78},
        'programa': 'ACNUR'
    },
    {
        'pais': 'Honduras',
        'departamento': 'Comayagua',
        'municipio': 'Comayagua',
        'lat': 14.4500,
        'lon': -87.6333,
        'cumplimiento': 84,
        'estado': '🟢',
        'categorias': {'Gestión de Casos': 83, 'SMAPS': 85, 'Entrega de Kits': 82, 'Fortalecimiento Liderazgo': 84},
        'programa': 'ACNUR'
    },
    
    # ===== HONDURAS - PMA (municipios adicionales) =====
    {
        'pais': 'Honduras',
        'departamento': 'Santa Bárbara',
        'municipio': 'Santa Bárbara (PMA)',
        'lat': 15.4750,
        'lon': -88.3750,
        'cumplimiento': 76,
        'estado': '🟡',
        'categorias': {'Objetivo 1': 76, 'Objetivo 2': 74, 'Objetivo 3': 50},
        'programa': 'PMA'
    },
    {
        'pais': 'Honduras',
        'departamento': 'Santa Bárbara',
        'municipio': 'Quimistán (PMA)',
        'lat': 15.3580,
        'lon': -88.4080,
        'cumplimiento': 76,
        'estado': '🟡',
        'categorias': {'Objetivo 1': 76, 'Objetivo 2': 74, 'Objetivo 3': 50},
        'programa': 'PMA'
    },
    {
        'pais': 'Honduras',
        'departamento': 'Ocotepeque',
        'municipio': 'Ocotepeque (PMA)',
        'lat': 14.4400,
        'lon': -89.2100,
        'cumplimiento': 79,
        'estado': '🟡',
        'categorias': {'Objetivo 1': 80, 'Objetivo 2': 77, 'Objetivo 3': 50},
        'programa': 'PMA'
    }
]

# ============ FUNCIONES DE PROCESAMIENTO ============

def get_estado(pct):
    if pct >= 85:
        return '🟢'
    elif pct >= 60:
        return '🟡'
    else:
        return '🔴'

def get_color(pct):
    if pct >= 85:
        return '#2ecc71'
    elif pct >= 60:
        return '#f1c40f'
    else:
        return '#e74c3c'

def get_programa_color(programa):
    colores = {
        'GT': '#1a5276',
        'ES': '#2e86c1',
        'ACNUR': '#1a5276',
        'PMA': '#27ae60'
    }
    return colores.get(programa, '#gray')

def procesar_data(data, proyecto):
    df = pd.DataFrame(data)
    df['% Cumplimiento'] = (df['logro'] / df['meta'] * 100).round(1)
    df['Estado'] = df['% Cumplimiento'].apply(get_estado)
    df['Proyecto'] = proyecto
    return df

# Procesar datos de proyectos
df_gt = procesar_data(data_gt, 'Guatemala')
df_es = procesar_data(data_es, 'El Salvador')
df_hn = procesar_data(data_hn, 'Honduras')

# DataFrame de municipios
df_municipios = pd.DataFrame(municipios_data)

# ============ FUNCIONES DE VISUALIZACIÓN ============

def crear_mapa(pais_filtro='Todos', programa_filtro='Todos'):
    """Crea un mapa de Folium con todos los municipios"""
    
    # Coordenadas centro de Centroamérica
    mapa = folium.Map(
        location=[14.5, -89.0],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Filtrar datos
    df_filtrado = df_municipios.copy()
    if pais_filtro != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['pais'] == pais_filtro]
    if programa_filtro != 'Todos':
        if programa_filtro == 'ACNUR':
            df_filtrado = df_filtrado[df_filtrado['programa'].isin(['ACNUR', 'GT', 'ES'])]
        elif programa_filtro == 'PMA':
            df_filtrado = df_filtrado[df_filtrado['programa'] == 'PMA']
        elif programa_filtro == 'GT':
            df_filtrado = df_filtrado[df_filtrado['programa'] == 'GT']
        elif programa_filtro == 'ES':
            df_filtrado = df_filtrado[df_filtrado['programa'] == 'ES']
    
    # Crear capa de calor
    heat_data = []
    
    # Agregar marcadores
    for _, row in df_filtrado.iterrows():
        # Calcular tamaño del círculo según cumplimiento
        radius = 8 + (row['cumplimiento'] / 100) * 12
        
        # Color según estado
        color = get_color(row['cumplimiento'])
        
        # Color del borde según programa
        borde_color = get_programa_color(row['programa'])
        
        # Determinar si es municipio de HN con PMA
        es_pma = row['programa'] == 'PMA'
        es_acnur = row['programa'] == 'ACNUR'
        
        # Crear popup con información detallada
        popup_text = f"""
        <div style="font-family: Arial, sans-serif; min-width: 280px; max-width: 350px;">
            <h4 style="margin: 0 0 8px 0; color: #2c3e50;">📍 {row['municipio']}</h4>
            <p style="margin: 0 0 4px 0; color: #34495e;">
                <b>🏛️ {row['departamento']}</b><br>
                <b>🌍 {row['pais']}</b>
            </p>
            <hr style="margin: 8px 0;">
            <p style="font-size: 18px; margin: 0 0 8px 0;">
                <b>📊 Cumplimiento:</b> {row['cumplimiento']}% {row['estado']}
            </p>
        """
        
        # Mostrar categorías según el programa
        if es_pma:
            popup_text += f"""
            <hr style="margin: 8px 0;">
            <p style="margin: 4px 0; font-size: 14px; color: #27ae60;">
                <b>🟢 PMA</b><br>
                📌 Objetivo 1: {row['categorias'].get('Objetivo 1', 0)}%<br>
                📌 Objetivo 2: {row['categorias'].get('Objetivo 2', 0)}%<br>
                📌 Objetivo 3: {row['categorias'].get('Objetivo 3', 0)}%
            </p>
            """
        elif es_acnur:
            popup_text += f"""
            <hr style="margin: 8px 0;">
            <p style="margin: 4px 0; font-size: 14px; color: #1a5276;">
                <b>🔵 ACNUR</b><br>
                📌 Gestión de Casos: {row['categorias'].get('Gestión de Casos', 0)}%<br>
                📌 SMAPS: {row['categorias'].get('SMAPS', 0)}%<br>
                📌 Entrega de Kits: {row['categorias'].get('Entrega de Kits', 0)}%<br>
                📌 Liderazgo: {row['categorias'].get('Fortalecimiento Liderazgo', 0)}%
            </p>
            """
        else:
            # GT o ES
            popup_text += f"""
            <hr style="margin: 8px 0;">
            <p style="margin: 4px 0; font-size: 14px;">
                <b>📋 Indicadores:</b><br>
                💧 WASH: {row['categorias'].get('WASH', 0)}%<br>
                👦 Niñez: {row['categorias'].get('Protección Niñez', 0)}%<br>
                👩 VBG: {row['categorias'].get('VBG', 0)}%<br>
                🌾 Seg. Alimentaria: {row['categorias'].get('Seguridad Alimentaria', 0)}%
            </p>
            """
        
        popup_text += """
            <hr style="margin: 8px 0;">
            <p style="font-size: 12px; color: #7f8c8d; margin: 0;">
                👆 Click para ver detalles en el panel
            </p>
        </div>
        """
        
        # Crear popup con HTML
        popup = folium.Popup(popup_text, max_width=350)
        
        # Agregar marcador circular
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=radius,
            popup=popup,
            color=borde_color,
            weight=3,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            tooltip=f"{row['municipio']}: {row['cumplimiento']}%"
        ).add_to(mapa)
        
        # Agregar datos para heatmap
        heat_data.append([row['lat'], row['lon'], row['cumplimiento'] / 100])
    
    # Agregar leyenda
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 9999; 
                background-color: white; padding: 15px; border-radius: 10px; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.2); font-family: Arial, sans-serif;
                min-width: 200px;">
        <div style="font-weight: bold; margin-bottom: 8px; color: #2c3e50;">
            🎯 Leyenda
        </div>
        <div style="display: flex; align-items: center; margin: 4px 0;">
            <div style="width: 14px; height: 14px; border-radius: 50%; 
                        background: #2ecc71; margin-right: 10px;"></div>
            <span>≥ 85% (Verde)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 4px 0;">
            <div style="width: 14px; height: 14px; border-radius: 50%; 
                        background: #f1c40f; margin-right: 10px;"></div>
            <span>60-84% (Amarillo)</span>
        </div>
        <div style="display: flex; align-items: center; margin: 4px 0;">
            <div style="width: 14px; height: 14px; border-radius: 50%; 
                        background: #e74c3c; margin-right: 10px;"></div>
            <span>&lt; 60% (Rojo)</span>
        </div>
        <hr style="margin: 8px 0;">
        <div style="font-size: 12px; color: #7f8c8d;">
            🔵 Borde Azul: GT / ACNUR<br>
            🟢 Borde Verde: PMA<br>
            🔵 Borde Azul Claro: ES
        </div>
    </div>
    '''
    
    mapa.get_root().html.add_child(folium.Element(legend_html))
    
    # Agregar HeatMap si hay datos
    if len(heat_data) > 5:
        HeatMap(heat_data, min_opacity=0.2, max_zoom=13, radius=25).add_to(mapa)
    
    return mapa

def mostrar_tabla_indicadores(df, proyecto, programa_filtro=None):
    """Muestra la tabla de indicadores"""
    df_display = df.copy()
    
    # Si hay filtro de programa y existe la columna 'programa'
    if programa_filtro and 'programa' in df_display.columns:
        if programa_filtro != 'Todos':
            df_display = df_display[df_display['programa'] == programa_filtro]
    
    # Seleccionar columnas a mostrar
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
    """Muestra alertas activas"""
    df_alerts = df.copy()
    if programa_filtro and 'programa' in df_alerts.columns and programa_filtro != 'Todos':
        df_alerts = df_alerts[df_alerts['programa'] == programa_filtro]
    
    alertas = df_alerts[df_alerts['Estado'] != '🟢']
    if len(alertas) > 0:
        for _, row in alertas.iterrows():
            if row['Estado'] == '🔴':
                st.error(
                    f"🔴 **CRÍTICO**: {row['indicador']} - "
                    f"{row['% Cumplimiento']}% ({row['logro']:.1f}/{row['meta']:.0f} {row['unidad']})"
                )
            else:
                st.warning(
                    f"🟡 **ATENCIÓN**: {row['indicador']} - "
                    f"{row['% Cumplimiento']}% ({row['logro']:.1f}/{row['meta']:.0f} {row['unidad']})"
                )
    else:
        st.success("✅ ¡Todos los indicadores están en verde! Excelente trabajo.")

def mostrar_detalle_municipio(municipio_seleccionado):
    """Muestra el detalle de un municipio seleccionado"""
    if municipio_seleccionado is None:
        st.info("👆 Haz clic en un municipio del mapa para ver sus detalles aquí")
        return
    
    # Buscar el municipio en los datos
    municipio = df_municipios[df_municipios['municipio'] == municipio_seleccionado]
    if len(municipio) == 0:
        st.warning("Municipio no encontrado")
        return
    
    row = municipio.iloc[0]
    
    st.subheader(f"📍 {row['municipio']}")
    st.caption(f"🏛️ {row['departamento']} · 🌍 {row['pais']}")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.metric("Cumplimiento Global", f"{row['cumplimiento']}%", delta=row['estado'])
    with col2:
        programa_label = "Programa"
        if row['programa'] == 'GT':
            programa_label = "🇬🇹 Guatemala"
        elif row['programa'] == 'ES':
            programa_label = "🇸🇻 El Salvador"
        elif row['programa'] == 'ACNUR':
            programa_label = "🔵 ACNUR"
        elif row['programa'] == 'PMA':
            programa_label = "🟢 PMA"
        st.metric("Programa", programa_label)
    with col3:
        st.write("")  # Espacio
    
    # Mostrar categorías
    st.markdown("**📋 Indicadores por categoría:**")
    
    if row['programa'] == 'PMA':
        cols = st.columns(3)
        objetivos = ['Objetivo 1', 'Objetivo 2', 'Objetivo 3']
        for col, obj in zip(cols, objetivos):
            with col:
                if obj in row['categorias']:
                    pct = row['categorias'][obj]
                    estado = get_estado(pct)
                    st.metric(
                        label=f"{estado} {obj}",
                        value=f"{pct}%"
                    )
    elif row['programa'] == 'ACNUR':
        cols = st.columns(4)
        categorias_hn = ['Gestión de Casos', 'SMAPS', 'Entrega de Kits', 'Fortalecimiento Liderazgo']
        for col, cat in zip(cols, categorias_hn):
            with col:
                if cat in row['categorias']:
                    pct = row['categorias'][cat]
                    estado = get_estado(pct)
                    st.metric(
                        label=f"{estado} {cat}",
                        value=f"{pct}%"
                    )
    else:
        # GT o ES
        cols = st.columns(4)
        categorias_std = ['WASH', 'Protección Niñez', 'VBG', 'Seguridad Alimentaria']
        for col, cat in zip(cols, categorias_std):
            with col:
                if cat in row['categorias']:
                    pct = row['categorias'][cat]
                    estado = get_estado(pct)
                    st.metric(
                        label=f"{estado} {cat}",
                        value=f"{pct}%"
                    )

def mostrar_graficos_proyecto(df, proyecto, programa_filtro=None):
    """Muestra gráficos del proyecto"""
    df_display = df.copy()
    if programa_filtro and 'programa' in df_display.columns and programa_filtro != 'Todos':
        df_display = df_display[df_display['programa'] == programa_filtro]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras
        fig = px.bar(
            df_display,
            x='indicador',
            y='% Cumplimiento',
            color='Estado',
            title=f"Cumplimiento por Indicador - {proyecto}",
            labels={'% Cumplimiento': 'Cumplimiento (%)', 'indicador': ''},
            height=350,
            color_discrete_map={'🟢': '#2ecc71', '🟡': '#f1c40f', '🔴': '#e74c3c'}
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            showlegend=False,
            yaxis_range=[0, 100]
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico de radar por categoría
        categorias = df_display['categoria'].unique()
        valores = []
        for cat in categorias:
            mask = df_display['categoria'] == cat
            pct_prom = df_display[mask]['% Cumplimiento'].mean()
            valores.append(pct_prom)
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=valores + [valores[0]],
            theta=list(categorias) + [categorias[0]],
            fill='toself',
            name=proyecto,
            line_color='#1a5276',
            fillcolor='rgba(26, 82, 118, 0.3)'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            height=350,
            title=f"Perfil de cumplimiento - {proyecto}"
        )
        st.plotly_chart(fig, use_container_width=True)

# ============ INTERFAZ PRINCIPAL ============

st.title("🌍 Monitoreo Humanitario - Centroamérica")

# ============ SIDEBAR ============
with st.sidebar:
    st.header("🎯 Filtros")
    
    # Filtro por país
    pais_filtro = st.selectbox(
        "🌍 País",
        options=['Todos', 'Guatemala', 'El Salvador', 'Honduras'],
        index=0
    )
    
    # Filtro por programa (dinámico)
    if pais_filtro == 'Honduras' or pais_filtro == 'Todos':
        programa_options = ['Todos', 'ACNUR', 'PMA']
    else:
        programa_options = ['Todos']
    
    programa_filtro = st.selectbox(
        "📂 Programa",
        options=programa_options,
        index=0
    )
    
    st.markdown("---")
    
    # Mostrar resumen global
    st.header("📊 Resumen Global")
    
    # Calcular cumplimiento por país
    gt_global = (df_gt['logro'].sum() / df_gt['meta'].sum() * 100)
    es_global = (df_es['logro'].sum() / df_es['meta'].sum() * 100)
    
    # HN - ACNUR
    df_hn_acnur = df_hn[df_hn['programa'] == 'ACNUR']
    hn_acnur_global = (df_hn_acnur['logro'].sum() / df_hn_acnur['meta'].sum() * 100) if len(df_hn_acnur) > 0 else 0
    
    # HN - PMA
    df_hn_pma = df_hn[df_hn['programa'] == 'PMA']
    hn_pma_global = (df_hn_pma['logro'].sum() / df_hn_pma['meta'].sum() * 100) if len(df_hn_pma) > 0 else 0
    
    st.metric("🇬🇹 Guatemala", f"{gt_global:.1f}%")
    st.metric("🇸🇻 El Salvador", f"{es_global:.1f}%")
    st.metric("🇭🇳 Honduras - ACNUR", f"{hn_acnur_global:.1f}%")
    st.metric("🇭🇳 Honduras - PMA", f"{hn_pma_global:.1f}%")
    
    st.markdown("---")
    st.caption("🗺️ Haz clic en cualquier municipio del mapa para ver sus detalles")

# ============ MAPA ============
st.subheader("🗺️ Mapa de Intervención")

# Crear y mostrar mapa
mapa = crear_mapa(pais_filtro, programa_filtro)
folium_static(mapa, width=None, height=600)

# ============ DETALLE DEL MUNICIPIO SELECCIONADO ============
st.markdown("---")
st.subheader("📋 Detalle del Municipio Seleccionado")

# Estado para mantener el municipio seleccionado
if 'municipio_seleccionado' not in st.session_state:
    st.session_state.municipio_seleccionado = None

# Mostrar detalle
mostrar_detalle_municipio(st.session_state.municipio_seleccionado)

# ============ DATOS DEL PROYECTO POR PAÍS ============
st.markdown("---")
st.subheader("📊 Datos de Proyectos por País")

# Pestañas para mostrar datos de proyectos
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
    
    # Selector de programa para HN
    hn_programa = st.radio(
        "📂 Seleccionar Programa",
        options=['Todos', 'ACNUR', 'PMA'],
        horizontal=True
    )
    
    # Mostrar según programa seleccionado
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
st.caption("🔵 ACNUR | 🟢 PMA | 👆 Haz clic en los municipios del mapa para ver detalles")
