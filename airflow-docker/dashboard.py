import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Conectar a la base de datos
conn = sqlite3.connect('C:/airflow-docker/dags/transacciones.db')
df = pd.read_sql_query("SELECT * FROM transacciones", conn)

# Sidebar para filtrar por rango de fechas
st.sidebar.header('Filtros')
fecha_min = pd.to_datetime(df['Fecha']).min()
fecha_max = pd.to_datetime(df['Fecha']).max()
rango_fechas = st.sidebar.date_input('Rango de fechas', [fecha_min, fecha_max])

# Filtrado de datos
if len(rango_fechas) == 2:
    df = df[(pd.to_datetime(df['Fecha']) >= pd.to_datetime(rango_fechas[0])) & 
            (pd.to_datetime(df['Fecha']) <= pd.to_datetime(rango_fechas[1]))]

# KPIs
st.title('Dashboard de Transacciones Financieras')
st.metric('Total de Transacciones', len(df))
st.metric('Importe Total', f"€{df['Importe'].sum():,.2f}")
st.metric('Saldo Promedio', f"€{df['Saldo'].mean():,.2f}")

# Gráficos
st.subheader('Evolución del Saldo')
fig, ax = plt.subplots()
df.groupby('Fecha')['Saldo'].mean().plot(ax=ax)
st.pyplot(fig)

st.subheader('Distribución de Importes por Concepto')
fig, ax = plt.subplots()
df.groupby('Concepto')['Importe'].sum().plot(kind='barh', ax=ax)
st.pyplot(fig)


# Tabla de datos
st.subheader('Detalle de Transacciones')
st.dataframe(df)
