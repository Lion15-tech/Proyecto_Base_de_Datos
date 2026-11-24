import sqlite3 

BASEDATOS= "GYM.db"

def conectar():
    return sqlite3.connect(BASEDATOS)

def crear_tabla():
    with conectar() as conect:
        conect.execute("""CREATE TABLE IF NOT EXISTS empleados(
        ID TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        telefono TEXT NOT NULL,
        contraseña TEXT NOT NULL,
        fecha_nacimiento TEXT NOT NULL)""")

def generar_id(nombre, apellido,  fecha_nacimiento):
    if not nombre or not apellido  or not fecha_nacimiento:
        raise ValueError("Todos los valores son obligatorios")

    inicial_apellido= apellido.strip()[0].upper()
    inicial_nombre= nombre.strip()[0].upper()
    fecha_limpia= fecha_nacimiento.strip().replace("/","").replace("-","")

    if len(fecha_limpia) != 8 or not fecha_limpia.isdigit():
        raise ValueError("La fecha debe tener format DD/MM/AAAA")

    return f"{inicial_apellido}{inicial_nombre}{fecha_limpia}"

def agregar_trabajador(nombre, apellido, telefono, contraseña, fecha_nacimiento):
    nuevo_id= generar_id(nombre,apellido,telefono,fecha_nacimiento)
    try:
        with conectar() as conect:
            conect.execute("INSERT INTO empleados (ID, nombre, apellio, telefono, tipo_membresia, fecha_nacimiento)"
                           "VALUES (?,?,?,?,?,?)",
                            (nuevo_id, nombre,apellido, telefono, contraseña,fecha_nacimiento))
    except sqlite3.IntegrityError:
        raise ValueError(f"EL ID {nuevo_id} ya existe. Cambia algún dato del cliente.")
    return nuevo_id

def modificar_cliente(ID, **valores):
    valor_protegido = {"ID"}
    valores_modificar = {"nombre", "apellido", "telefono", "contraseña", "fecha_nacimiento"}

    if not valores:
        raise ValueError("No se porporcionaron los valores a modificar")
    if valor_protegido & valores.keys():
        raise ValueError("El ID no se puede modificar")
    if not valores.keys() <= valores_modificar:
        invalidos = valores.keys() - valores_modificar
        raise ValueError(f"Campos invalidos {invalidos}")

    actu = ", ".join(f"{columna} = ?" for columna in valores.keys())
    meter_valor= list(valores.values()) + [ID]
    actu_trabajador= f"UPDATE empleados SET {actu} WHERE ID = ?"

    with conectar() as conect:
        cusor= conect.execute(actu_trabajador, meter_valor)
        return cusor.rowcount > 0

def eliminar_trabajador(ID):
    with conectar() as conect:
        cursor= conect.execute("DELATE FROM empleados WHERE ID = ?", (ID,))
        return cursor.rowcount > 0

def ver_trabajadores():
    with conectar() as  conect:
        return conect.execute("SELECT * FROM empleados").fetchall()
