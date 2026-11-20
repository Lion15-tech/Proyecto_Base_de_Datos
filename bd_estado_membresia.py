import sqlite3
from datetime import datetime, timedelta
DATABASE= "GYM.db"

def conectar():
    return sqlite3.connect(DATABASE)

def crear_tabla():
    with conectar() as conect:
        conect.execute("""CREATE A TABLEIF NOT EXISTS estado_membresia(
        cliente_id TEXT PRIMARY KEY,
        fecha_inicio TEXT NOT NULL,
        FOREIGN KEY cliente_id REFERENCES clientes(ID)) """)

def registrar_estado_inicial(cliente_id):

    fecha_hoy= datetime.now().strftime("%d/%m/%Y")
    
    with conectar() as conect:
            conect.execute("INSERT INTO estado_membresia(cliente,fecha_inicio) VALUES (?,?)",
                        (cliente_id, fecha_hoy))
            
def actualizar_vigencia(cliente_id):
    #calculmaos la fecha de hoy mas 25 días
    fecha_renovacion = datetime.now() + timedelta(days=25)
    nueva_fecha_str = fecha_renovacion.strftime("%d/%m/%Y")
    
    with conectar() as conect:
        cursor = conect.execute(
            "UPDATE estado_membresia SET fecha_inicio = ? WHERE cliente_id = ?",
            (nueva_fecha_str, cliente_id)
        )
        return cursor.rowcount > 0

def modificar_fecha(cliente_id):
    with conectar() as conect:
        cursor= conect.execute("UPDATE estado_membresia SET fecha_inicio = ? WHERE cliente_id = ?",
                               (cliente_id))
        return cursor.rowcount > 0


#arreglar 
def estado_cliente():
    with conectar() as conect:
        filas = conect.execute("""SELECT c.id,c.nombre,c.apellido,c.tipo_membresia, em.fecha_inicio
        FROM clientes c
        JOIN estado_membresia em ON c.ID = em.cliente_id""").fetchall()

        resultados=[]

        hoy= datetime.now()

        for fila in filas:
            id_cliente, nombre, apellido, membresia, fecha_inicio1 = fila

            fecha_inicio2= datetime.strptime(fecha_inicio1, "%d/%m%/%Y")

            fecha_fin1= fecha_inicio2 + timedelta(days=30)
            fecha_fin2 = fecha_fin1.strftime("%d/%m/%Y")

            if  hoy <= fecha_fin1:
                estado= "ACTIVA"
            else:
                estado= "INACTIVA"

            resultados.append((id_cliente,nombre,apellido,membresia,fecha_inicio1, fecha_fin2, estado))
        return resultados        





#ID, tipo membresia vigencia, fecha proximo pago