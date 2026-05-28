import streamlit as st
import pandas as pd
import plotly.express as px
import ast

#para pdf
#from reportlab.platypus import SimpleDocTemplate
#from reportlab.platypus import Paragraph, Spacer, Image
#from reportlab.lib.styles import getSampleStyleSheet


# ----------------------------
# CONFIG PAGINA
# ----------------------------
st.set_page_config(
    page_title="Dashboard Financiero",
    layout="wide"
)

st.title("📊 Dashboard de Gastos")

# ----------------------------
# CARGAR DATOS
# ----------------------------
df = pd.read_csv("data/raw/datos_gasto.csv")

# ----------------------------
# LIMPIEZA
# ----------------------------

df['categoria'] = df['categoria'].apply(ast.literal_eval)
df['metodoPago'] = df['metodoPago'].apply(ast.literal_eval)
df['usuario'] = df['usuario'].apply(ast.literal_eval)
df['comercio'] = df['comercio'].apply(ast.literal_eval)

# nuevas columnas
df['categoria_nombre'] = df['categoria'].apply(lambda x: x['nombre'])
df['forma_pago'] = df['metodoPago'].apply(lambda x: x['formaPago'])
df['comercio_nombre'] = df['comercio'].apply(lambda x: x['nombreComercio'])
df['usuario_nombre'] = df['usuario'].apply(lambda x: x['nombre'])
df['usuario_id'] = df['usuario'].apply(lambda x: x['id'])

df['usuario_label'] = (
    df['usuario_nombre'] +
    " - " +
    df['usuario_id'].astype(str)
)

# fechas
df['fecha'] = pd.to_datetime(
    df['fecha'],
    format='mixed',
    errors='coerce'
)

df['mes'] = df['fecha'].dt.month_name()

# ----------------------------
# SIDEBAR
# ----------------------------

st.sidebar.header("Filtros")

usuarios = ['Todos'] + list(df['usuario_label'].unique())

usuario_seleccionado = st.sidebar.selectbox(
    "Selecciona usuario",
    usuarios
)

# dataframe filtrado
if usuario_seleccionado == 'Todos':
    df_filtrado = df
else:
    df_filtrado = df[
        df['usuario_label'] == usuario_seleccionado
    ]


# ----------------------------
# KPIs
# ----------------------------
total_gastado = df_filtrado['valor'].sum()
total_transacciones = len(df_filtrado)

col1, col2 = st.columns(2)

col1.metric("💰 Total Gastado", f"${total_gastado:,.0f}")
col2.metric("🧾 Transacciones", total_transacciones)


# ----------------------------
# GASTOS POR CATEGORIA
# ----------------------------
st.subheader("Gastos por Categoría")

gastos_categoria = (
    df_filtrado.groupby('categoria_nombre')['valor']
    .sum()
    .reset_index()
)

fig_categoria = px.bar(
    gastos_categoria,
    x='categoria_nombre',
    y='valor',
    color='categoria_nombre'
)

st.plotly_chart(fig_categoria, use_container_width=True)

# ----------------------------
# METODOS DE PAGO
# ----------------------------
st.subheader("Métodos de Pago")

fig_pago = px.pie(
    df_filtrado,
    names='forma_pago'
)

st.plotly_chart(fig_pago, use_container_width=True)

# ----------------------------
# EVOLUCION TEMPORAL
# ----------------------------
st.subheader("Evolución de Gastos")

gastos_fecha = (
    df_filtrado.groupby('fecha')['valor']
    .sum()
    .reset_index()
)

fig_fecha = px.line(
    gastos_fecha,
    x='fecha',
    y='valor'
)

st.plotly_chart(fig_fecha, use_container_width=True)

# ----------------------------
# TOP COMERCIOS
# ----------------------------
st.subheader("Top Comercios")

top_comercios = (
    df_filtrado.groupby('comercio_nombre')['valor']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_comercio = px.bar(
    top_comercios,
    x='comercio_nombre',
    y='valor',
    color='valor'
)

st.plotly_chart(fig_comercio, use_container_width=True)


