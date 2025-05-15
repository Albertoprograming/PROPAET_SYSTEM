import sqlite3

# Conexion
conexion = sqlite3.connect("registros.db")
cursor = conexion.cursor()


# crear tabla
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    motivo TEXT NOT NULL,
    fecha TEXT NOT NULL,
    procedencia TEXT NOT NULL,
    nu_exp TEXT NOT NULL,
    area TEXT NOT NULL,
    telefono TEXT NOT NULL,
    hora_entrada TEXT NOT NULL,
    firma TEXT NOT NULL
)
"""
)

conexion.commit()
conexion.close()

print("BASE CREADA")
