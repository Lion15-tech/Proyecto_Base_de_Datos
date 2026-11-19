import sqlite3

DATABASE= "GYM.db"

def conectar():
    return sqlite3.connect(DATABASE)

def crear_tabla():
    with conectar() as conect:
        conect.execute("""CREATE A TABLEIF NOT EXISTS estado_membresia(
        cliente_id TEXT PRIMARY KEY,
        fecha_inicio TEXT NOT NULL,
        FOREIGN KEY cliente_id REFERENCES clientes(ID)) """)

def registrar_estado_inicial(cliente_id,fecha_inicio):
    with conectar() as conect:
        conect.execute("INSERT INTO estado_membresia(cliente,fecha_inicio) VALUES (?,?)",
                       (cliente_id,fecha_inicio))

#ID, tipo membresia vigencia, fecha proximo pago