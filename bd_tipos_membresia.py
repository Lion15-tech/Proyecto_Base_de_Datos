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
            conect.execute("INSERT INTO tipo_membresia(nombre,precio), VALUES(?,?)",
                        (nombre,precio))
    except sqlite3.IntegrityError:
        raise ValueError(f"La membresia {nombre} ya existe") #esto no se si sirva pero no lo quites
    

def ver_membresias():
    with conectar() as conect:
        conect.execute("""
        FROM tipo_membresia tm
        LEFT JOIN clientes c ON c.tipo_membresia = tm.nombre
        SELECT tm.nombre, tm.precio, COUNT(c.ID) AS cantidad_clientes
        GROUP BY t,.nombre, tm.precio""").fetchall()