import pandas as pd
import streamlit as st

RUTA_DATOS = "data/dataset_limpio.csv"


@st.cache_data
def cargar_datos():
    df = pd.read_csv(RUTA_DATOS, index_col=0)
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    return df
