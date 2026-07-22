import streamlit as st
import pandas as pd

st.set_page_config(page_title="Monitoreo Humanitario", layout="wide")
st.title("🌍 Monitoreo Humanitario - Guatemala")

# ============ DATOS ============
data = {
    'categoria': [
        'Agua, Saneamiento e Higiene', 
        'Agua, Saneamiento e Higiene',
        'Protección de la Niñez', 
        'Protección de la Niñez', 
        'Protección de la Niñez',
        'Protección - VBG',
        'Seguridad Alimentaria', 
        'Seguridad Alimentaria', 
        'Seguridad Alimentaria'
    ],
    'indicador': [
        'Kits de WASH distribuidos',
        'Personas con mensajes WASH',
        'Niños/as con apoyo psicosocial',
        'Personas capacitadas',
        'Personas en espacios amigables',
        'Staff capacitado en VBG',
        'Transferencias GLOBAL',
        'Transferencias CASH',
        'Valor total transferencias'
    ],
    'unidad': ['Kits', 'Personas', 'Niños', 'Personas', 'Personas', 'Personas', 'Personas', 'Personas', 'USD'],
    'meta': [500, 2000, 300, 150, 400, 80, 1200, 800, 50000],
    'logro': [320, 1850, 210, 95, 380, 45, 1050, 540, 38500]
}

df = pd.DataFrame(data)
df['% Cumplimiento'] = (df['logro'] / df['meta'] * 100).round(1)

# Semáforo
def get_estado(pct):
    if pct >= 85:
        return '🟢'
    elif pct >= 60:
        return '🟡'
    else:
        return '🔴'

df['Estado'] = df['% Cumplimiento'].apply(get_estado)

# ============ SIDEBAR ============
st.sidebar.title("📊 Resumen")
st.sidebar.metric("Total Indicadores", len(df))
promedio_global = (df['logro'].sum() / df['meta'].sum() * 100)
st.sidebar.metric("Cumplimiento Global", f"{promedio_global:.1f}%")

# Leyenda
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎨 Leyenda")
st.sidebar.markdown("🟢 ≥ 85% - En meta")
st.sidebar.markdown("🟡 60-84% - Atención")
st.sidebar.markdown("🔴 < 60% - Crítico")

# ============ TARJETAS DE CATEGORÍAS ============
st.subheader("📋 Estado por Categoría")
categorias = df['categoria'].unique()
cols = st.columns(len(categorias))

for idx, (col, cat) in enumerate(zip(cols, categorias)):
    with col:
        mask = df['categoria'] == cat
        pct_prom = df[mask]['% Cumplimiento'].mean()
        estado = get_estado(pct_prom)
        nombre_corto = cat[:20] + "..." if len(cat) > 20 else cat
        st.metric(
            label=f"{estado} {nombre_corto}",
            value=f"{pct_prom:.0f}%"
        )

# ============ TABLA PRINCIPAL ============
st.subheader("📊 Detalle de Indicadores")
st.dataframe(
    df[['categoria', 'indicador', 'unidad', 'meta', 'logro', '% Cumplimiento', 'Estado']],
    use_container_width=True,
    hide_index=True
)

# ============ GRÁFICO DE BARRAS (NATIVO) ============
st.subheader("📊 Cumplimiento por Indicador")
chart_data = df.set_index('indicador')[['% Cumplimiento']]
st.bar_chart(chart_data, height=400, use_container_width=True)

# ============ ALERTAS ============
st.subheader("🚨 Alertas Activas")

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

st.caption(f"📅 Actualizado: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
