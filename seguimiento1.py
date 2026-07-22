import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# ----------------- CONFIGURACIÓN DE PÁGINA -----------------
st.set_page_config(
    page_title="Monitoreo Humanitario",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- INICIALIZAR DATOS -----------------
ARCHIVO_DATOS = "datos/indicadores.csv"

def cargar_datos():
    """Carga los datos desde CSV o crea estructura inicial"""
    if os.path.exists(ARCHIVO_DATOS):
        return pd.read_csv(ARCHIVO_DATOS)
    else:
        # Datos iniciales de ejemplo
        datos = pd.DataFrame({
            'categoria': [
                'Agua, Saneamiento e Higiene', 'Agua, Saneamiento e Higiene',
                'Protección de la Niñez', 'Protección de la Niñez', 'Protección de la Niñez',
                'Protección - VBG',
                'Seguridad Alimentaria', 'Seguridad Alimentaria', 'Seguridad Alimentaria'
            ],
            'indicador': [
                'Kits de WASH/higiene distribuidos',
                'Personas que reciben mensajes de WASH',
                'Niños/as que reciben apoyo psicosocial',
                'Personas capacitadas en sesiones informativas',
                'Personas que acceden a espacios amigables',
                'Staff de socios capacitados en VBG',
                'Personas con transferencias GLOBAL',
                'Personas con transferencias CASH',
                'Valor total transferencias monetarias'
            ],
            'unidad': [
                'Kits', 'Personas', 'Niños', 'Personas', 'Personas',
                'Personas', 'Personas', 'Personas', 'USD'
            ],
            'meta': [500, 2000, 300, 150, 400, 80, 1200, 800, 50000],
            'logro': [320, 1850, 210, 95, 380, 45, 1050, 540, 38500],
            'fecha_actualizacion': [datetime.now().strftime('%Y-%m-%d')] * 9
        })
        # Crear carpeta si no existe
        os.makedirs("datos", exist_ok=True)
        datos.to_csv(ARCHIVO_DATOS, index=False)
        return datos

def guardar_datos(df):
    """Guarda los datos en CSV"""
    df.to_csv(ARCHIVO_DATOS, index=False)

# ----------------- FUNCIONES DE CÁLCULO -----------------
def calcular_semaforo(pct):
    """Asigna color según porcentaje de cumplimiento"""
    if pct >= 85:
        return "🟢", "Verde"
    elif pct >= 60:
        return "🟡", "Amarillo"
    else:
        return "🔴", "Rojo"

def calcular_estado_categoria(df, categoria):
    """Calcula el estado promedio de una categoría"""
    mask = df['categoria'] == categoria
    pcts = df[mask]['logro'] / df[mask]['meta'] * 100
    promedio = pcts.mean()
    semaforo, _ = calcular_semaforo(promedio)
    return promedio, semaforo

# ----------------- SIDEBAR: DATOS GENERALES -----------------
st.sidebar.title("🌍 Monitoreo Humanitario")
st.sidebar.markdown("---")
st.sidebar.markdown(f"**📅 Fecha:** {datetime.now().strftime('%d/%m/%Y')}")

# Cargar datos
df = cargar_datos()

# Mostrar resumen en sidebar
total_indicadores = len(df)
promedio_global = (df['logro'].sum() / df['meta'].sum()) * 100
semaforo_global, _ = calcular_semaforo(promedio_global)

st.sidebar.metric("📊 Indicadores", total_indicadores)
st.sidebar.metric("🎯 Cumplimiento Global", f"{promedio_global:.1f}%", 
                  delta=f"{semaforo_global}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Leyenda")
st.sidebar.markdown("🟢 ≥ 85% - En meta")
st.sidebar.markdown("🟡 60-84% - Atención")
st.sidebar.markdown("🔴 < 60% - Crítico")

# ----------------- MAIN CONTENT -----------------
st.title("🌍 Dashboard de Monitoreo Humanitario")
st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ----- SECCIÓN 1: TARJETAS DE CATEGORÍAS -----
st.subheader("📋 Estado por Categoría")

col1, col2, col3, col4 = st.columns(4)

categorias = df['categoria'].unique()
colores_meta = ['#2ecc71', '#f1c40f', '#e74c3c', '#3498db']

for idx, (col, cat) in enumerate(zip([col1, col2, col3, col4], categorias)):
    with col:
        pct, semaforo = calcular_estado_categoria(df, cat)
        # Extraer nombre corto para mostrar
        nombre_corto = cat.split('-')[0].strip()
        if len(nombre_corto) > 20:
            nombre_corto = nombre_corto[:20] + "..."
        
        st.markdown(f"""
        <div style="
            background: {colores_meta[idx % len(colores_meta)]}22;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid {colores_meta[idx % len(colores_meta)]};
            margin-bottom: 10px;
        ">
            <h4 style="margin:0; color:{colores_meta[idx % len(colores_meta)]}">{semaforo} {nombre_corto}</h4>
            <p style="font-size:24px; margin:5px 0; font-weight:bold;">{pct:.0f}%</p>
            <p style="font-size:12px; margin:0; color:gray;">Cumplimiento</p>
        </div>
        """, unsafe_allow_html=True)

# ----- SECCIÓN 2: TABLA COMPLETA CON EDITOR -----
st.subheader("📊 Detalle de Indicadores")
st.caption("Edita los valores de 'Logro' directamente en la tabla")

# Mostrar tabla con editor
columnas_editar = ['categoria', 'indicador', 'unidad', 'meta', 'logro']
df_edit = df[columnas_editar].copy()

# Agregar columna de porcentaje
df_edit['% Cumplimiento'] = (df_edit['logro'] / df_edit['meta'] * 100).round(1)

# Agregar semáforo
df_edit['Estado'] = df_edit['% Cumplimiento'].apply(
    lambda x: '🟢' if x >= 85 else '🟡' if x >= 60 else '🔴'
)

# Editor interactivo
df_edit = st.data_editor(
    df_edit,
    use_container_width=True,
    column_config={
        "categoria": st.column_config.TextColumn("Categoría", disabled=True),
        "indicador": st.column_config.TextColumn("Indicador", disabled=True),
        "unidad": st.column_config.TextColumn("Unidad", disabled=True),
        "meta": st.column_config.NumberColumn("Meta", disabled=True),
        "logro": st.column_config.NumberColumn("Logro", step=1, min_value=0),
        "% Cumplimiento": st.column_config.NumberColumn("%", format="%.1f", disabled=True),
        "Estado": st.column_config.TextColumn("Estado", disabled=True),
    },
    hide_index=True,
    num_rows="dynamic"
)

# Botón para guardar cambios
if st.button("💾 Guardar cambios", type="primary", use_container_width=True):
    # Actualizar solo la columna 'logro' en el DataFrame original
    for idx, row in df_edit.iterrows():
        if idx < len(df):
            df.loc[idx, 'logro'] = row['logro']
    df['fecha_actualizacion'] = datetime.now().strftime('%Y-%m-%d')
    guardar_datos(df)
    st.success("✅ Datos guardados correctamente")
    st.rerun()

# ----- SECCIÓN 3: GRÁFICOS -----
st.subheader("📈 Visualizaciones")

tab1, tab2, tab3 = st.tabs(["📊 Barras", "🎯 Radar", "📉 Evolución"])

with tab1:
    # Gráfico de barras: Meta vs Logro por indicador
    fig_bar = px.bar(
        df,
        x='indicador',
        y=['meta', 'logro'],
        barmode='group',
        title="Meta vs Logro por Indicador",
        labels={'value': 'Cantidad', 'variable': 'Tipo'},
        color_discrete_map={'meta': '#3498db', 'logro': '#2ecc71'},
        height=400
    )
    fig_bar.update_layout(xaxis_tickangle=-45, showlegend=True)
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    # Gráfico de radar por categoría
    datos_radar = []
    for cat in categorias:
        mask = df['categoria'] == cat
        pct_prom = (df[mask]['logro'].sum() / df[mask]['meta'].sum()) * 100
        datos_radar.append({'categoria': cat.split('-')[0].strip(), 'cumplimiento': pct_prom})
    
    df_radar = pd.DataFrame(datos_radar)
    
    fig_radar = px.line_polar(
        df_radar,
        r='cumplimiento',
        theta='categoria',
        line_close=True,
        title="Cumplimiento por Categoría (Radar)",
        range_r=[0, 100],
        color_discrete_sequence=['#e74c3c'],
        height=400
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with tab3:
    # Simulación de evolución (para demostración)
    st.info("📌 Los datos de evolución se generan automáticamente al actualizar semanalmente")
    
    # Crear datos simulados de progreso
    semanas = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']
    datos_evolucion = []
    for cat in categorias[:2]:  # Mostrar solo 2 categorías para ejemplo
        mask = df['categoria'] == cat
        pct = (df[mask]['logro'].sum() / df[mask]['meta'].sum()) * 100
        # Simular progreso semanal (variación aleatoria)
        import random
        random.seed(42)
        base = pct - 15
        for i, sem in enumerate(semanas):
            datos_evolucion.append({
                'categoria': cat.split('-')[0].strip(),
                'semana': sem,
                'cumplimiento': min(100, base + (i+1) * random.uniform(3, 8))
            })
    
    df_evolucion = pd.DataFrame(datos_evolucion)
    fig_evol = px.line(
        df_evolucion,
        x='semana',
        y='cumplimiento',
        color='categoria',
        title="Evolución Semanal (Simulada)",
        markers=True,
        height=400
    )
    fig_evol.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig_evol, use_container_width=True)

# ----- SECCIÓN 4: ALERTAS -----
st.subheader("🚨 Alertas Activas")

# Identificar indicadores críticos y en atención
df['porcentaje'] = (df['logro'] / df['meta'] * 100)
df_alerta = df.copy()
df_alerta['estado'] = df_alerta['porcentaje'].apply(
    lambda x: 'Crítico' if x < 60 else 'Atención' if x < 85 else 'OK'
)

alertas = df_alerta[df_alerta['estado'].isin(['Crítico', 'Atención'])]

if len(alertas) > 0:
    for idx, row in alertas.iterrows():
        if row['estado'] == 'Crítico':
            st.error(f"🔴 **CRÍTICO**: {row['indicador']} - {row['logro']:.0f}/{row['meta']:.0f} ({row['porcentaje']:.0f}%)")
        else:
            st.warning(f"🟡 **ATENCIÓN**: {row['indicador']} - {row['logro']:.0f}/{row['meta']:.0f} ({row['porcentaje']:.0f}%)")
else:
    st.success("✅ ¡Todos los indicadores están en verde! Excelente trabajo.")

# ----- FOOTER -----
st.markdown("---")
st.caption("💡 Desarrollado con Streamlit · Datos almacenados localmente en CSV")

# ----------------- SIDEBAR: EXPORTAR DATOS -----------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Exportar")

if st.sidebar.button("📤 Descargar CSV"):
    csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="⬇️ Descargar datos",
        data=csv,
        file_name=f"monitoreo_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

if st.sidebar.button("🔄 Restablecer datos de ejemplo"):
    if st.sidebar.checkbox("¿Estás seguro?"):
        os.remove(ARCHIVO_DATOS)
        st.rerun()
