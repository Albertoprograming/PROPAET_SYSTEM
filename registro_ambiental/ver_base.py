import sqlite3

# Conectar a la base
conn = sqlite3.connect("registros.db")
cursor = conn.cursor()

# Mostrar todas las tablas (estructura)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tablas:", cursor.fetchall())

# Ver contenido de la tabla 'usuarios'
cursor.execute("SELECT * FROM registros;")
print("Contenido:")
for fila in cursor.fetchall():
    print(fila)

conn.close()
