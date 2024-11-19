import streamlit as st
import pandas as pd
import sqlite3

st.title("Prueba de Streamlit")
st.write("¡Todo está funcionando correctamente!")

# Prueba de conexión SQLite
conexion = sqlite3.connect(":memory:")
st.write("SQLite está funcionando. Conexión en memoria creada.")
