import sqlite3

DATABASE= "GYM.db"

def conectar():
    return sqlite3.connect(DATABASE)

def crear_tabla():
    with conectar() as conect:
        conect.execute("""CREATE TABLE IF NOT EXISTS tipo_membresia(
        nombre TEXT PRIMARY KEY,
        precio REAL NOT NULL)""")

def añadir_membresia(nombre,precio):
    try:
        with conectar() as conect:
            conect.execute("INSERT INTO tipo_membresia(nombre,precio) VALUES(?,?)",
                        (nombre,precio))
    except sqlite3.IntegrityError:
        raise ValueError(f"La membresia {nombre} ya existe") #esto no se si sirva pero no lo quites
  
#Para cada tipo de membresía, muéstrame su nombre, 
# su precio, y cuántos clientes tienen esa membresía. 
# Incluye también las membresías que no tienen ningún cliente (con 0).

def ver_membresia():
    with conectar() as conect:
        return conect.execute("""
        SELECT tm.nombre, tm.precio, COUNT (c.ID) AS cantidad_clientes
        FROM tipo_membresia tm
        LEFT JOIN clientes c ON c.tipo_membresia = tm.nombre
        GROUP BY tm.nombre, tm.precio""").fetchall()

#--SELECT--
#COUNT (c.ID) cuenta cuántos ID de clientes hay en el grupo actual
#AS cantidad_clientes   le pone un apodo si no seria COUNT(c.ID) 
#FROM de esta tabla y la apoda tm para facilidas

def obtener_nombres_membresias():
    with conectar() as conect:
        nombres = conect.execute("SELECT nombre FROM tipo_membresia").fetchall()
        obt_nombre = [fila[0] for fila in nombres]
        return obt_nombre
if __name__ == "__main__":
    crear_tabla()
    nuevo4= añadir_membresia("prueba", 10)

"""
SELECT ...      ← 1. qué columnas quieres
FROM ...        ← 2. de qué tabla
LEFT JOIN ...   ← 3. qué otras tablas pegas
WHERE ...       ← 4. filtros (opcional)
GROUP BY ...    ← 5. cómo agrupas
ORDER BY ...    ← 6. cómo ordenas (opcional)"""