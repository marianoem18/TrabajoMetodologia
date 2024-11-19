import streamlit as st
from database_manager import initialize_database

# Inicializar la base de datos
initialize_database()

# Interfaz de usuario simple para verificar la conexión
st.title("Prueba de Streamlit")
st.write("¡Todo está funcionando correctamente!")

# Puedes agregar funcionalidades adicionales aquí...

