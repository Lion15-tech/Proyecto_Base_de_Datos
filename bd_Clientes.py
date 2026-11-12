import sqlite3 #se importea sqlite3 #UNIQUE (trabajadores)

DATABASE = "GYM.db" #variable ahorrar tiempo

def conectar(): #Funcion no escribir conexion completo
    return sqlite3.connect(DATABASE)

def crear_tabla():
    with conectar() as conect: #NOT NULL significa no se puede quedar vacia
        conect.execute("""CREATE TABLE IF NOT EXISTS clientes(
            ID TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT NOT NULL,
            tipo_membresia TEXT NOT NULL, 
            fecha_nacimiento TEXT NOT NULL)""") 
    #crea una tabla llamada clientes si no existe, id es primary key (no se debe repetir su valor) nombre, apellido, telefono, tipo de membresia, fecha nacimiento

def generar_id(nombre, apellido, tipo_membresia, fecha_nacimiento):
    if not nombre or not apellido or not tipo_membresia or not fecha_nacimiento: #Todos los valores deben estar para generar id uncio
        raise ValueError("Todos los valores son obligatorios >:(") 

    inicial_apellido  = apellido.strip()[0].upper() #strip borra espacio primero y ultimo
    inicial_nombre  = nombre.strip()[0].upper() #[0] agarra el primer caracter
    inicial_membresia = tipo_membresia.strip()[0].upper() #.upper la vuelve mayuscula
    fecha_limpia = fecha_nacimiento.strip().replace("/", "").replace("-", "").replace("_","").replace(".","")
    #Remplaza posibles separaciones usuario

    if len(fecha_limpia) != 8 or not fecha_limpia.isdigit(): #si la cantidad de caracteres de fecha es mdistinta a 8 o si hay algo que no es digito (isdigit)
        raise ValueError("La fecha debe tener formato DD/MM/AAAA")

    return f"{inicial_apellido}{inicial_nombre}{inicial_membresia}{fecha_limpia}" #da valores en la varible que lo llama

def agregar_cliente(nombre, apellido, telefono, tipo_membresia, fecha_nacimiento): #Valores que se pasaran 
    nuevo_id = generar_id(nombre, apellido, tipo_membresia, fecha_nacimiento) #se llama funcion generar ID
    try:
        with conectar() as conect:
            conect.execute(
                "INSERT INTO clientes (ID, nombre, apellido, telefono, tipo_membresia, fecha_nacimiento) " #insertar valors en tabla clientes (molde)
                "VALUES (?, ?, ?, ?, ?, ?)", #rodrigo no toques esto!
                (nuevo_id, nombre, apellido, telefono, tipo_membresia, fecha_nacimiento)) #valores reales qye pasará
    except sqlite3.IntegrityError: #tipo error cuando se rompe molde
        raise ValueError(f"El ID {nuevo_id} ya existe. Cambia algún dato del cliente.")
    return nuevo_id

def modificar_cliente(ID, **valores):
    valor_protegido = {"ID"}
    valores_modificar = {"nombre", "apellido", "telefono", "tipo_membresia", "fecha_nacimiento"}

    if not valores:
        raise ValueError("No se proporcionaron los valores a modificar")
    if valor_protegido & valores.keys():
        raise ValueError("El ID no se puede modificar")
    if not valores.keys() <= valores_modificar:
        invalidos = valores.keys() - valores_modificar
        raise ValueError(f"Campos invalidos {invalidos}")

    actu = ", ".join(f"{columna} = ?" for columna in valores.keys())
    meter_valor = list(valores.values()) + [ID]
    actu_cliente = f"UPDATE clientes SET {actu} WHERE ID = ?"

    with conectar() as conect:
        cursor = conect.execute(actu_cliente, meter_valor)
        return cursor.rowcount > 0

def eliminar_cliente(ID):
    with conectar() as conect:
        cur = conect.execute("DELETE FROM clientes WHERE ID = ?", (ID,))
        return cur.rowcount > 0

def ver_clientes():
    with conectar() as conect:
        return conect.execute("SELECT * FROM clientes").fetchall()


if __name__ == "__main__":
    crear_tabla()
    nuevo = agregar_cliente("Carlos", "Colon", "44217249863", "Basica", "10112026")