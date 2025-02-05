import streamlit as st
import pandas as pd
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Conexión a la base de datos
conn = sqlite3.connect('./dags/transacciones.db')
df = pd.read_sql_query("SELECT * FROM transacciones", conn)

# Preprocesamiento de datos
st.title('Predicción de Gastos Futuros')
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Año'] = df['Fecha'].dt.year
df['Mes'] = df['Fecha'].dt.month

# Filtrado de columnas relevantes
df_modelo = df[['Año', 'Mes', 'Importe']]

# Agrupar por año y mes
agrupado = df_modelo.groupby(['Año', 'Mes']).sum().reset_index()

# Variables independientes (X) y dependiente (y)
X = agrupado[['Año', 'Mes']]
y = agrupado['Importe']

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Predicciones
y_pred = modelo.predict(X_test)

# Visualización
st.subheader('Comparación de Valores Reales vs. Predichos')
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
ax.set_xlabel('Valores Reales')
ax.set_ylabel('Valores Predichos')
st.pyplot(fig)

# Predicción para el próximo mes
ultimo_mes = agrupado[['Año', 'Mes']].max()
proximo_mes = pd.DataFrame({
    'Año': [ultimo_mes['Año'] + 1 if ultimo_mes['Mes'] == 12 else ultimo_mes['Año']],
    'Mes': [1 if ultimo_mes['Mes'] == 12 else ultimo_mes['Mes'] + 1]
})

prediccion_futura = modelo.predict(proximo_mes)
st.subheader('Predicción de Gastos para el Próximo Mes')
st.metric(label='Gasto Estimado', value=f"€{prediccion_futura[0]:,.2f}")
