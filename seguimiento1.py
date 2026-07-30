import streamlit as st
import pandas as pd

st.set_page_config(page_title="Monitoreo Humanitario - 3 Países", layout="wide")
st.title("🌍 Monitoreo Humanitario - Guatemala, El Salvador y Honduras")

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
    'logro': [2800, 14500, 135, 2400, 78, 8200, 7800, 680000]
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
    'logro': [8500, 18500, 9200, 42, 230, 720, 42, 2600, 310, 1450, 185, 27500, 10500, 1200000, 10500, 42, 2800, 440]
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
    'logro': [145, 295, 5100, 2550, 108]
}

# ============ FUNCIONES ============
def procesar_data(data, proyecto):
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

df_gt = procesar_data(data_gt, 'Guatemala')
df_es = procesar_data(data_es, 'El Salvador')
df_hn = procesar_data(data_hn, 'Honduras')

# ============ INTERFAZ ============
tab1, tab2, tab3 = st.tabs(["🇬🇹 Guatemala", "🇸🇻 El Salvador", "🇭🇳 Honduras"])

with tab1:
    st.header("🇬🇹 Guatemala")
    st.caption("Período: Mayo - Noviembre 2026")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pct = df_gt[df_gt['categoria']=='WASH']['% Cumplimiento'].mean()
        st.metric("🟢 WASH (29%)", f"{pct:.0f}%")
    with col2:
        pct = df_gt[df_gt['categoria']=='Protección Niñez']['% Cumplimiento'].mean()
        st.metric("🟢 Niñez (10%)", f"{pct:.0f}%")
    with col3:
        pct = df_gt[df_gt['categoria']=='VBG']['% Cumplimiento'].mean()
        st.metric("🟢 VBG (3%)", f"{pct:.0f}%")
    with col4:
        pct = df_gt[df_gt['categoria']=='Seguridad Alimentaria']['% Cumplimiento'].mean()
        st.metric("🟢 Seg. Alim (58%)", f"{pct:.0f}%")
    
    st.dataframe(df_gt[['categoria', 'indicador', 'unidad', 'meta', 'logro', '% Cumplimiento', 'Estado']], 
                 use_container_width=True, hide_index=True)
    
    # Alertas
    alertas = df_gt[df_gt['Estado'] != '🟢']
    for _, row in alertas.iterrows():
        if row['Estado'] == '🔴':
            st.error(f"🔴 {row['indicador']}: {row['% Cumplimiento']}%")
        else:
            st.warning(f"🟡 {row['indicador']}: {row['% Cumplimiento']}%")

with tab2:
    st.header("🇸🇻 El Salvador")
    st.caption("Período: Mayo - Noviembre 2026")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        pct = df_es[df_es['categoria']=='WASH']['% Cumplimiento'].mean()
        st.metric("WASH 25%", f"{pct:.0f}%")
    with col2:
        pct = df_es[df_es['categoria']=='Protección']['% Cumplimiento'].mean()
        st.metric("Protección 4%", f"{pct:.0f}%")
    with col3:
        pct = df_es[df_es['categoria']=='VBG']['% Cumplimiento'].mean()
        st.metric("VBG 4%", f"{pct:.0f}%")
    with col4:
        pct = df_es[df_es['categoria']=='Protección Niñez']['% Cumplimiento'].mean()
        st.metric("Niñez 11%", f"{pct:.0f}%")
    with col5:
        pct = df_es[df_es['categoria']=='Seguridad Alimentaria']['% Cumplimiento'].mean()
        st.metric("Seg. Alim 56%", f"{pct:.0f}%")
    
    st.dataframe(df_es[['categoria', 'indicador', 'unidad', 'meta', 'logro', '% Cumplimiento', 'Estado']], 
                 use_container_width=True, hide_index=True)
    
    alertas = df_es[df_es['Estado'] != '🟢']
    for _, row in alertas.iterrows():
        if row['Estado'] == '🔴':
            st.error(f"🔴 {row['indicador']}: {row['% Cumplimiento']}%")
        else:
            st.warning(f"🟡 {row['indicador']}: {row['% Cumplimiento']}%")

with tab3:
    st.header("🇭🇳 Honduras")
    st.caption("Período: Mayo - Octubre 2026")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        pct = df_hn[df_hn['categoria']=='Gestión de Casos']['% Cumplimiento'].mean()
        st.metric("Gestión Casos", f"{pct:.0f}%")
    with col2:
        pct = df_hn[df_hn['categoria']=='SMAPS']['% Cumplimiento'].mean()
        st.metric("SMAPS", f"{pct:.0f}%")
    with col3:
        pct = df_hn[df_hn['categoria']=='Entrega de Kits']['% Cumplimiento'].mean()
        st.metric("Kits", f"{pct:.0f}%")
    with col4:
        pct = df_hn[df_hn['categoria']=='Fortalecimiento Liderazgo']['% Cumplimiento'].mean()
        st.metric("Liderazgo", f"{pct:.0f}%")
    
    st.dataframe(df_hn[['categoria', 'indicador', 'unidad', 'meta', 'logro', '% Cumplimiento', 'Estado']], 
                 use_container_width=True, hide_index=True)
    
    alertas = df_hn[df_hn['Estado'] != '🟢']
    for _, row in alertas.iterrows():
        if row['Estado'] == '🔴':
            st.error(f"🔴 {row['indicador']}: {row['% Cumplimiento']}%")
        else:
            st.warning(f"🟡 {row['indicador']}: {row['% Cumplimiento']}%")

st.caption("📅 Datos simulados - Última actualización: 30 de julio 2026")
