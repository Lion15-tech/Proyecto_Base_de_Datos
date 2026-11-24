import sqlite3
from datetime import datetime, timedelta

DATABASE = "GYM.db"

def conectar():
    return sqlite3.connect(DATABASE)

def crear_tabla():
    with conectar() as conect:
        conect.execute("""CREATE TABLE IF NOT EXISTS estado_membresia(
        cliente_id TEXT PRIMARY KEY,
        fecha_inicio TEXT NOT NULL,
        fecha_vencimiento TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(ID))""")
        try:
            conect.execute("ALTER TABLE estado_membresia ADD COLUMN fecha_vencimiento TEXT")
        except sqlite3.OperationalError:
            pass

def registrar_estado_inicial(cliente_id, fecha_inicio=None):
    fecha_hoy = fecha_inicio if fecha_inicio else datetime.now().strftime("%d/%m/%Y")
    vencimiento = (datetime.strptime(fecha_hoy, "%d/%m/%Y") + timedelta(days=30)).strftime("%d/%m/%Y")
    with conectar() as conect:
        conect.execute(
            "INSERT INTO estado_membresia(cliente_id, fecha_inicio, fecha_vencimiento) VALUES (?,?,?)",
            (cliente_id, fecha_hoy, vencimiento)
        )

def renovar_membresia(cliente_id):
    with conectar() as conect:
        fila = conect.execute(
            "SELECT fecha_inicio, fecha_vencimiento FROM estado_membresia WHERE cliente_id = ?",
            (cliente_id,)
        ).fetchone()
        if not fila:
            return False

        fecha_inicio, fecha_venc = fila
        hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if fecha_venc:
            venc_dt = datetime.strptime(fecha_venc, "%d/%m/%Y")
        else:
            venc_dt = datetime.strptime(fecha_inicio, "%d/%m/%Y") + timedelta(days=30)

        base = venc_dt if venc_dt >= hoy else hoy
        nuevo_venc = (base + timedelta(days=30)).strftime("%d/%m/%Y")

        cursor = conect.execute(
            "UPDATE estado_membresia SET fecha_vencimiento = ? WHERE cliente_id = ?",
            (nuevo_venc, cliente_id)
        )
        return cursor.rowcount > 0

def desactivar_membresia(cliente_id):
    ayer = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
    with conectar() as conect:
        cursor = conect.execute(
            "UPDATE estado_membresia SET fecha_vencimiento = ? WHERE cliente_id = ?",
            (ayer, cliente_id)
        )
        return cursor.rowcount > 0

def eliminar_estado(cliente_id):
    with conectar() as conect:
        cursor = conect.execute("DELETE FROM estado_membresia WHERE cliente_id = ?", (cliente_id,))
        return cursor.rowcount > 0

def estado_cliente():
    with conectar() as conect:
        filas = conect.execute("""SELECT c.id, c.nombre, c.apellido, c.tipo_membresia, em.fecha_inicio, em.fecha_vencimiento
        FROM clientes c
        JOIN estado_membresia em ON c.ID = em.cliente_id""").fetchall()

        resultados = []
        hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        for fila in filas:
            id_cliente, nombre, apellido, membresia, fecha_inicio1, fecha_venc1 = fila

            if fecha_venc1:
                fecha_fin1 = datetime.strptime(fecha_venc1, "%d/%m/%Y")
                fecha_fin2 = fecha_venc1
            else:
                fecha_fin1 = datetime.strptime(fecha_inicio1, "%d/%m/%Y") + timedelta(days=30)
                fecha_fin2 = fecha_fin1.strftime("%d/%m/%Y")

            estado = "ACTIVA" if hoy <= fecha_fin1 else "INACTIVA"
            resultados.append((id_cliente, nombre, apellido, membresia, fecha_inicio1, fecha_fin2, estado))
        return resultados