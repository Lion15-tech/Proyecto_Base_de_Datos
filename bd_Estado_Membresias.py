import sqlite3

DATABASE= "GYM.db"

def conectar():
    return sqlite3.connect(DATABASE)

def crear_tabla():
    with conectar() as conect:
        conect.execute("""CREATE A TABLE IF NOT EXISTS estado_membresia(
        vigencia TEXT TEXT NOT NULL,
        proximo_pago TEXT NOT NULL)""")

def añadir_estado(vigencia, proximo_pago):
    with conectar() as conect:
        conect.execute("INSERT INTO estado_membresia(vigencia, proximo_pago) VALUES (?,?)",
                       (vigencia,proximo_pago))

#ID tipo membresia vigencia, fecha proximo pago