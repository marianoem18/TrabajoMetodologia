import sqlite3

# Función para conectarte a la base de datos
def connect_to_db():
    """
    Establece una conexión con la base de datos SQLite.
    Si la base de datos no existe, SQLite la crea automáticamente.
    """
    connection = sqlite3.connect('database.db')  # Nombre del archivo SQLite
    return connection

# Función para inicializar la base de datos con el script SQL
def initialize_database():
    """
    Inicializa la base de datos ejecutando el script SQL para crear las tablas.
    Lee el archivo SQL y ejecuta todas las instrucciones definidas.
    """
    connection = connect_to_db()  # Conexión a la base de datos
    cursor = connection.cursor()

    try:
        # Cargar y ejecutar el script SQL desde un archivo
        with open('metodologiaaa.sql', 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
        
        cursor.executescript(sql_script)  # Ejecutar el script completo
        connection.commit()  # Guardar los cambios
        print("Base de datos inicializada correctamente.")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        connection.close()   # Cerrar la conexión
