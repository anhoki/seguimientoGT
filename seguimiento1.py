import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============ CONFIGURACIÓN ============
st.set_page_config(
    page_title="Monitoreo Humanitario - 3 Países",
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

# HN - Honduras
data_hn = {
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
    'peso': [0, 0, 0, 0, 0]  # No aplica
}

# ============ FUNCIONES DE PROCESAMIENTO ============
def procesar_data(data, proyecto):
    """Procesa los datos y calcula porcentajes y semáforos"""
    df = pd.DataFrame(data)
    df['% Cumplimiento'] = (df['logro'] / df['meta'] * 100).round(1)
    
    def get_estado(pct):
        if pct >= 85:
            return '🟢'
        elif pct >= 60:
            return '🟡'
        else:
            return '🔴'
    
    df['Estado'] = df['% Cumplimiento'].apply(get_estado)
    df['Proyecto'] = proyecto
    return df

# Procesar cada proyecto
df_gt = procesar_data(data_gt, 'Guatemala')
df_es = procesar_data(data_es, 'El Salvador')
df_hn = procesar_data(data_hn, 'Honduras')

# ============ FUNCIONES DE VISUALIZACIÓN ============
def mostrar_resumen_categorias(df, proyecto):
    """Muestra tarjetas de resumen por categoría"""
    if proyecto == 'Honduras':
        categorias = df['categoria'].unique()
        cols = st.columns(len(categorias))
        for idx, (col, cat) in enumerate(zip(cols, categorias)):
            with col:
                mask = df['categoria'] == cat
                pct_prom = df[mask]['% Cumplimiento'].mean()
                estado = '🟢' if pct_prom >= 85 else '🟡' if pct_prom >= 60 else '🔴'
                st.metric(
                    label=f"{estado} {cat}",
                    value=f"{pct_prom:.0f}%"
                )
    else:
        # Para GT y ES: mostrar con porcentajes de inversión
        categorias_pesos = {
            'WASH': 29 if proyecto == 'Guatemala' else 25,
            'Protección Niñez': 10 if proyecto == 'Guatemala' else 11,
            'VBG': 3 if proyecto == 'Guatemala' else 4,
            'Seguridad Alimentaria': 58 if proyecto == 'Guatemala' else 56,
            'Protección': 4 if proyecto == 'El Salvador' else 0
        }
        
        categorias = df['categoria'].unique()
        cols = st.columns(len(categorias))
        for idx, (col, cat) in enumerate(zip(cols, categorias)):
            with col:
                mask = df['categoria'] == cat
                pct_prom = df[mask]['% Cumplimiento'].mean()
                estado = '🟢' if pct_prom >= 85 else '🟡' if pct_prom >= 60 else '🔴'
                peso = categorias_pesos.get(cat, 0)
                label = f"{estado} {cat}"
                if peso > 0:
                    label += f" ({peso}%)"
                st.metric(
                    label=label,
                    value=f"{pct_prom:.0f}%"
                )

def mostrar_tabla_indicadores(df):
    """Muestra la tabla de indicadores"""
    st.dataframe(
        df[['categoria', 'indicador', 'unidad', 'meta', 'logro', '% Cumplimiento', 'Estado']],
        use_container_width=True,
        hide_index=True,
        column_config={
            'categoria': 'Categoría',
            'indicador': 'Indicador',
            'unidad': 'Unidad',
            'meta': st.column_config.NumberColumn('Meta', format="%d"),
            'logro': st.column_config.NumberColumn('Logro', format="%d"),
            '% Cumplimiento': st.column_config.NumberColumn('%', format="%.1f"),
            'Estado': 'Estado'
        }
    )

def mostrar_grafico_barras(df):
    """Muestra gráfico de barras"""
    fig = px.bar(
        df,
        x='indicador',
        y='% Cumplimiento',
        color='Estado',
        title="Cumplimiento por Indicador",
        labels={'% Cumplimiento': 'Cumplimiento (%)', 'indicador': ''},
        height=400,
        color_discrete_map={'🟢': '#2ecc71', '🟡': '#f1c40f', '🔴': '#e74c3c'}
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        yaxis_range=[0, 100]
    )
    st.plotly_chart(fig, use_container_width=True)

def mostrar_alertas(df):
    """Muestra alertas activas"""
    alertas = df[df['Estado'] != '🟢']
    if len(alertas) > 0:
        for _, row in alertas.iterrows():
            if row['Estado'] == '🔴':
                st.error(
                    f"🔴 **CRÍTICO**: {row['indicador']} - "
                    f"{row['% Cumplimiento']}% ({row['logro']:.0f}/{row['meta']:.0f} {row['unidad']})"
                )
            else:
                st.warning(
                    f"🟡 **ATENCIÓN**: {row['indicador']} - "
                    f"{row['% Cumplimiento']}% ({row['logro']:.0f}/{row['meta']:.0f} {row['unidad']})"
                )
    else:
        st.success("✅ ¡Todos los indicadores están en verde! Excelente trabajo.")

def mostrar_grafico_radar(df, proyecto):
    """Muestra gráfico de radar por categoría"""
    categorias = df['categoria'].unique()
    valores = []
    for cat in categorias:
        mask = df['categoria'] == cat
        pct_prom = df[mask]['% Cumplimiento'].mean()
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

def mostrar_comparativa():
    """Muestra gráfico comparativo entre países"""
    # Preparar datos comparativos
    comparativa = []
    
    # GT
    for cat in df_gt['categoria'].unique():
        mask = df_gt['categoria'] == cat
        pct = df_gt[mask]['% Cumplimiento'].mean()
        comparativa.append({'País': 'Guatemala', 'Categoría': cat, 'Cumplimiento': pct})
    
    # ES
    for cat in df_es['categoria'].unique():
        mask = df_es['categoria'] == cat
        pct = df_es[mask]['% Cumplimiento'].mean()
        comparativa.append({'País': 'El Salvador', 'Categoría': cat, 'Cumplimiento': pct})
    
    # HN
    for cat in df_hn['categoria'].unique():
        mask = df_hn['categoria'] == cat
        pct = df_hn[mask]['% Cumplimiento'].mean()
        comparativa.append({'País': 'Honduras', 'Categoría': cat, 'Cumplimiento': pct})
    
    df_comp = pd.DataFrame(comparativa)
    
    fig = px.bar(
        df_comp,
        x='Categoría',
        y='Cumplimiento',
        color='País',
        barmode='group',
        title="Comparativa de Cumplimiento por País",
        labels={'Cumplimiento': 'Cumplimiento (%)'},
        height=400,
        color_discrete_map={
            'Guatemala': '#1a5276',
            'El Salvador': '#2e86c1',
            'Honduras': '#85c1e9'
        }
    )
    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)

def mostrar_comparativa_general():
    """Muestra métricas comparativas generales"""
    # Calcular cumplimiento global por país
    gt_global = (df_gt['logro'].sum() / df_gt['meta'].sum() * 100)
    es_global = (df_es['logro'].sum() / df_es['meta'].sum() * 100)
    hn_global = (df_hn['logro'].sum() / df_hn['meta'].sum() * 100)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        estado = '🟢' if gt_global >= 85 else '🟡' if gt_global >= 60 else '🔴'
        st.metric(
            label="🇬🇹 Guatemala",
            value=f"{gt_global:.1f}%",
            delta=f"{estado} General"
        )
    
    with col2:
        estado = '🟢' if es_global >= 85 else '🟡' if es_global >= 60 else '🔴'
        st.metric(
            label="🇸🇻 El Salvador",
            value=f"{es_global:.1f}%",
            delta=f"{estado} General"
        )
    
    with col3:
        estado = '🟢' if hn_global >= 85 else '🟡' if hn_global >= 60 else '🔴'
        st.metric(
            label="🇭🇳 Honduras",
            value=f"{hn_global:.1f}%",
            delta=f"{estado} General"
        )

# ============ INTERFAZ PRINCIPAL ============
st.title("🌍 Monitoreo Humanitario - Guatemala, El Salvador y Honduras")

# Resumen ejecutivo de todos los proyectos
st.subheader("📊 Resumen Ejecutivo Regional")
mostrar_comparativa_general()
st.markdown("---")

# Pestañas por proyecto
tab1, tab2, tab3, tab4 = st.tabs(["🇬🇹 Guatemala", "🇸🇻 El Salvador", "🇭🇳 Honduras", "📈 Comparativa Regional"])

with tab1:
    st.header("🇬🇹 Guatemala")
    st.caption("Período: Mayo - Noviembre 2026")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📋 Estado por Categoría")
        mostrar_resumen_categorias(df_gt, 'Guatemala')
    with col2:
        st.subheader("📊 Distribución")
        st.info("WASH: 29% | Niñez: 10% | VBG: 3% | Seg. Alimentaria: 58%")
    
    st.markdown("---")
    st.subheader("📊 Detalle de Indicadores")
    mostrar_tabla_indicadores(df_gt)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Cumplimiento por Indicador")
        mostrar_grafico_barras(df_gt)
    with col2:
        st.subheader("🎯 Perfil de Cumplimiento")
        mostrar_grafico_radar(df_gt, 'Guatemala')
    
    st.subheader("🚨 Alertas Activas")
    mostrar_alertas(df_gt)

with tab2:
    st.header("🇸🇻 El Salvador")
    st.caption("Período: Mayo - Noviembre 2026")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📋 Estado por Categoría")
        mostrar_resumen_categorias(df_es, 'El Salvador')
    with col2:
        st.subheader("📊 Distribución")
        st.info("WASH: 25% | Protección: 4% | VBG: 4% | Niñez: 11% | Seg. Alim: 56%")
    
    st.markdown("---")
    st.subheader("📊 Detalle de Indicadores")
    mostrar_tabla_indicadores(df_es)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Cumplimiento por Indicador")
        mostrar_grafico_barras(df_es)
    with col2:
        st.subheader("🎯 Perfil de Cumplimiento")
        mostrar_grafico_radar(df_es, 'El Salvador')
    
    st.subheader("🚨 Alertas Activas")
    mostrar_alertas(df_es)

with tab3:
    st.header("🇭🇳 Honduras")
    st.caption("Período: Mayo - Octubre 2026")
    
    st.subheader("📋 Estado por Categoría")
    mostrar_resumen_categorias(df_hn, 'Honduras')
    
    st.markdown("---")
    st.subheader("📊 Detalle de Indicadores")
    mostrar_tabla_indicadores(df_hn)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Cumplimiento por Indicador")
        mostrar_grafico_barras(df_hn)
    with col2:
        st.subheader("🎯 Perfil de Cumplimiento")
        mostrar_grafico_radar(df_hn, 'Honduras')
    
    st.subheader("🚨 Alertas Activas")
    mostrar_alertas(df_hn)

with tab4:
    st.header("📈 Comparativa Regional")
    st.caption("Comparación de cumplimiento entre los 3 países")
    
    st.subheader("📊 Resumen General")
    mostrar_comparativa_general()
    
    st.markdown("---")
    st.subheader("📊 Comparativa por Categoría")
    mostrar_comparativa()
    
    # Tabla comparativa detallada
    st.subheader("📋 Comparativa detallada")
    
    # Preparar datos para tabla comparativa
    comp_data = []
    for df, pais in [(df_gt, 'Guatemala'), (df_es, 'El Salvador'), (df_hn, 'Honduras')]:
        for _, row in df.iterrows():
            comp_data.append({
                'País': pais,
                'Categoría': row['categoria'],
                'Indicador': row['indicador'],
                '% Cumplimiento': row['% Cumplimiento'],
                'Estado': row['Estado']
            })
    
    df_comp_detalle = pd.DataFrame(comp_data)
    
    # Pivot para ver comparativa
    pivot_df = df_comp_detalle.pivot_table(
        index=['Categoría', 'Indicador'],
        columns='País',
        values='% Cumplimiento'
    ).round(1)
    
    st.dataframe(pivot_df, use_container_width=True)

# ============ FOOTER ============
st.markdown("---")
st.caption("📅 Datos simulados - Última actualización: 30 de julio 2026")
st.caption("💡 GT y ES: Mayo - Noviembre 2026 | HN: Mayo - Octubre 2026")
