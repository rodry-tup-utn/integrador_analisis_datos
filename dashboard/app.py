import streamlit as st
import pandas as pd
import plotly.express as px

from utils import cargar_datos

st.set_page_config(
    page_title="Dashboard Comercial",
    page_icon="📊",
    layout="wide",
)

df = cargar_datos()

st.title("📊 Reporte Ejecutivo")
st.markdown("Dashboard interactivo con datos de ventas de la cadena comercial.")
st.divider()

# SIDEBAR

st.sidebar.header("Filtros")

fecha_min = df["Fecha"].min()
fecha_max = df["Fecha"].max()

# Estados por defecto
if "fecha_desde" not in st.session_state:
    st.session_state["fecha_desde"] = fecha_min
    st.session_state["fecha_hasta"] = fecha_max
    st.session_state["paises"] = sorted(df["Pais"].unique())
    st.session_state["categorias"] = sorted(df["Categoria"].unique())
    st.session_state["metodos_pago"] = sorted(df["Metodo_Pago"].unique())
    st.session_state["indices"] = sorted(df["Indice_Constancia"].unique())

# Boton limpieza de filtros
if st.sidebar.button("🔄 Limpiar todos los filtros"):
    st.session_state["fecha_desde"] = fecha_min
    st.session_state["fecha_hasta"] = fecha_max
    st.session_state["paises"] = sorted(df["Pais"].unique())
    st.session_state["categorias"] = sorted(df["Categoria"].unique())
    st.session_state["metodos_pago"] = sorted(df["Metodo_Pago"].unique())
    st.session_state["indices"] = sorted(df["Indice_Constancia"].unique())
    st.rerun()

#  Widgets
fecha_desde = st.sidebar.date_input(
    "Fecha desde",
    key="fecha_desde",
    min_value=fecha_min,
    max_value=fecha_max,
)
fecha_hasta = st.sidebar.date_input(
    "Fecha hasta",
    key="fecha_hasta",
    min_value=fecha_min,
    max_value=fecha_max,
)

paises = st.sidebar.multiselect(
    "País",
    options=sorted(df["Pais"].unique()),
    key="paises",
)

categorias = st.sidebar.multiselect(
    "Categoría",
    options=sorted(df["Categoria"].unique()),
    key="categorias",
)

metodos_pago = st.sidebar.multiselect(
    "Método de pago",
    options=sorted(df["Metodo_Pago"].unique()),
    key="metodos_pago",
)

indices = st.sidebar.multiselect(
    "Indice de constancia",
    options=sorted(df["Indice_Constancia"].unique()),
    key="indices",
)

#  FILTRADO

mask = (
    (df["Fecha"] >= pd.Timestamp(fecha_desde))
    & (df["Fecha"] <= pd.Timestamp(fecha_hasta))
    & (df["Pais"].isin(paises))
    & (df["Categoria"].isin(categorias))
    & (df["Metodo_Pago"].isin(metodos_pago))
    & (df["Indice_Constancia"].isin(indices))
)

df_filtrado = df[mask].copy()

if df_filtrado.empty:
    st.warning("No hay datos con los filtros seleccionados.")
    st.stop()

#  KPIs

total_ventas = df_filtrado["Venta_Total"].sum()
total_ganancia = df_filtrado["Ganancia_Bruta"].sum()
total_transacciones = len(df_filtrado)
ticket_promedio = total_ventas / total_transacciones

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Venta Total", f"${total_ventas:,.2f}")

with col2:
    st.metric("Ganancia Bruta", f"${total_ganancia:,.2f}")

with col3:
    st.metric("Transacciones", f"{total_transacciones:,}")

with col4:
    st.metric("Ticket Promedio", f"${ticket_promedio:,.2f}")

st.divider()

#  GRAFICOS

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📈 Evolución de Ventas por Mes")
    ventas_mes = df_filtrado.groupby("mes_texto")["Venta_Total"].sum().reset_index()
    fig_linea = px.line(
        ventas_mes,
        x="mes_texto",
        y="Venta_Total",
        markers=True,
    )
    fig_linea.update_layout(
        xaxis_title="Mes",
        yaxis_title="Venta Total ($)",
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_linea, use_container_width=True)

with col_right:
    st.markdown("### 📊 Ventas por Categoría")
    ventas_cat = (
        df_filtrado.groupby("Categoria")["Venta_Total"]
        .sum()
        .reset_index()
        .sort_values("Venta_Total", ascending=False)
    )
    fig_barras_cat = px.bar(
        ventas_cat,
        x="Categoria",
        y="Venta_Total",
        color="Categoria",
        text_auto=".2s",  # type: ignore
    )
    fig_barras_cat.update_layout(
        xaxis_title="Categoría",
        yaxis_title="Venta Total ($)",
        showlegend=False,
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_barras_cat, use_container_width=True)

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.markdown("### 🏆 Top 10 Productos más Vendidos")
    top_productos = (
        df_filtrado.groupby("Producto")["Venta_Total"]
        .sum()
        .reset_index()
        .sort_values("Venta_Total", ascending=False)
        .head(10)
    )
    fig_top = px.bar(
        top_productos,
        x="Venta_Total",
        y="Producto",
        orientation="h",
        color="Venta_Total",
        color_continuous_scale="blues",
        text_auto=".2s",  # type: ignore
    )
    fig_top.update_layout(
        xaxis_title="Venta Total ($)",
        yaxis_title="",
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    fig_top.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_top, use_container_width=True)

with col_right2:
    st.markdown("### 🌍 Ventas por País")
    ventas_pais = (
        df_filtrado.groupby("Pais")["Venta_Total"]
        .sum()
        .reset_index()
        .sort_values("Venta_Total", ascending=False)
    )
    fig_pais = px.bar(
        ventas_pais,
        x="Pais",
        y="Venta_Total",
        color="Pais",
        text_auto=".2s",  # type: ignore
    )
    fig_pais.update_layout(
        xaxis_title="País",
        yaxis_title="Venta Total ($)",
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_pais, use_container_width=True)

st.divider()

col_pie, col_cliente = st.columns(2)

with col_pie:
    st.markdown("### 🥧 Distribución por Método de Pago")
    metodo = df_filtrado.groupby("Metodo_Pago")["Venta_Total"].sum().reset_index()
    fig_pie = px.pie(
        metodo,
        names="Metodo_Pago",
        values="Venta_Total",
        hole=0.4,
    )
    fig_pie.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_cliente:
    st.markdown("### 👥 Ventas por Tipo de Cliente")
    ventas_cliente = (
        df_filtrado.groupby("Indice_Constancia")["Venta_Total"]
        .sum()
        .reset_index()
        .sort_values("Venta_Total", ascending=False)
    )
    fig_cliente = px.bar(
        ventas_cliente,
        x="Indice_Constancia",
        y="Venta_Total",
        color="Indice_Constancia",
        text_auto=".2s",  # type: ignore
        color_discrete_map={
            "01-Fiel (VIP)": "#2ecc71",
            "02-Regular": "#3498db",
            "03-Ocasional": "#e74c3c",
        },
    )
    fig_cliente.update_layout(
        xaxis_title="Tipo de Cliente",
        yaxis_title="Venta Total ($)",
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    st.plotly_chart(fig_cliente, use_container_width=True)

st.divider()

#  TABLA FINAL

st.markdown("### 📋 Detalle de Operaciones")
st.dataframe(
    df_filtrado.drop(columns=["ID_Transaccion"]),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Fecha": st.column_config.DateColumn("Fecha"),
        "Venta_Total": st.column_config.NumberColumn("Venta Total", format="$%.2f"),
        "Ganancia_Bruta": st.column_config.NumberColumn(
            "Ganancia Bruta", format="$%.2f"
        ),
        "Costo_Total": st.column_config.NumberColumn("Costo Total", format="$%.2f"),
    },
)
