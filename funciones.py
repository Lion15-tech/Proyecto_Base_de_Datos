import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import estilos as est
import bd_Clientes as bd_c
import bd_tipos_membresia as tm
import bd_estado_membresia as bam

def inicializar_tablas():
    bd_c.crear_tabla()
    tm.crear_tabla()
    bam.crear_tabla()
    for nombre, precio in [("Básico", 100), ("Estandar", 250), ("Ultra", 500)]:
        try:
            tm.añadir_membresia(nombre, precio)
        except ValueError:
            pass
    try:
        bd_c.agregar_cliente("Carlos", "Colon", "4421724986", "Básico", "10/11/2026")
    except ValueError:
        pass
    for cliente in bd_c.ver_clientes():
        try:
            bam.registrar_estado_inicial(cliente[0])
        except Exception:
            pass


class Verificar:
    def __init__(self, quien, tipo):
        self.quien = quien
        self.tipo = tipo
        self.es_valido = False

    def verif(self, evento):
        texto = self.quien.get().strip()

        if not texto:
            self.quien.config(bg="#FFFFFF") 
            self.es_valido = False
            return True

        if self.tipo == "numeros":
            self.es_valido = texto.isdigit()
        elif self.tipo == "telefono":
            self.es_valido = texto.isdigit() and len(texto) == 10
        elif self.tipo == "texto":
            self.es_valido = texto.replace(" ", "").isalpha()
        elif self.tipo == "fecha":  # dd/mm/aaaa
            if len(texto) == 10:
                try:
                    datetime.strptime(texto, "%d/%m/%Y")
                    self.es_valido = True
                except ValueError:
                    self.es_valido = False
            else:
                self.es_valido = False

        if self.es_valido == True:
            self.quien.config(bg="#FFFFFF")
        else:
            self.quien.config(bg="#C22525")


def efectito_chido(boton):
    boton.bind("<Enter>", lambda efect: boton.config(bg=est.COLOR_BOTON_EFECTO))
    boton.bind("<Leave>", lambda efect: boton.config(bg=est.COLOR_BOTON))


def crear_boton(padre, texto, comando, fuente_texto, color_fondo, color_texto, color_boton_presionado):
    boton = tk.Button(padre, 
                      text=texto, 
                      command=comando,
                      font=fuente_texto,
                      bg=color_fondo, 
                      fg=color_texto,
                      activebackground=color_boton_presionado)
    efectito_chido(boton)
    return boton


def confirmar_accion(ventana):
    return messagebox.askyesno("¿Seguro?", "¿Estás seguro que deseas realizar esta acción?", parent=ventana)


def confirmar_accion_eliminar(ventana):
    return messagebox.askyesno("¿Seguro?", "¿Estás seguro que deseas realizar esta acción? Esto NO se puede deshacer.", parent=ventana)


def campo(panel_form, etiqueta, tipo_validacion): # Etiqueta + entry
    tk.Label(panel_form,
             text=etiqueta,
             font=est.FUENTE_TEXTO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=5,
      ).pack(padx=5)    
    
    e = tk.Entry(panel_form, justify="center")
    e.pack(padx=15, pady=15)    
    
    validador = Verificar(e, tipo_validacion)
    
    # Usamos KeyRelease para leer el texto ya escrito
    e.bind("<KeyRelease>", validador.verif)
    return e


### ===================================================== ###
#                          VENTANAS                         #
### ===================================================== ###

## Ventana Clientes 
def Crear_Ventana_Clientes(ventana_padre):
    ventana_padre.withdraw()
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Clientes")
    ventana.geometry("1300x700")
    ventana.resizable(False, False)
    ventana.configure(bg=est.COLOR_FONDO)
    ventana.protocol("WM_DELETE_WINDOW",
                     lambda: (ventana_padre.deiconify(), ventana.destroy()))

    id_cliente_seleccionado = tk.StringVar()

    # ---- Panel de la tabla (derecha) ----
    panel_tabla = tk.Frame(ventana, bg=est.FONDO_TABLA)
    panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)

    # ---- Panel para modificar (izquierda) ----
    panel_para_modificar = tk.Frame(ventana, bg=est.COLOR_FONDO, padx=15, pady=15)
    panel_para_modificar.pack(side="left", fill="y")

    tk.Label(panel_para_modificar, text="CLIENTES",
             font=est.FUENTE_SUBTITULO, bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO, pady=20).pack(padx=15)

    entrada_nombre = campo(panel_para_modificar, "Nombre:", "texto")
    entrada_apellido = campo(panel_para_modificar, "Apellido:", "texto")
    entrada_telefono = campo(panel_para_modificar, "Teléfono:", "telefono")

    tk.Label(panel_para_modificar,
             text="Tipo Membresia",
             font=est.FUENTE_TEXTO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=5).pack(padx=5)
    membresias = [""] + tm.obtener_nombres_membresias()
    menu_seleccion = ttk.Combobox(panel_para_modificar,
                                  values=membresias,
                                  state="readonly")
    menu_seleccion.set("")
    menu_seleccion.pack(pady=10)

    entrada_fecha = campo(panel_para_modificar, "Fecha nacimiento (DD/MM/AAAA):", "fecha")

    # ---- Treeview con 6 columnas ----
    columnas = ("ID", "Nombre", "Apellido", "Teléfono", "Membresía", "Fecha Nac.")
    tabla = ttk.Treeview(panel_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=130)

    scrollbar = ttk.Scrollbar(panel_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(expand=True, fill="both")

    # ---- Auxiliares ----
    def cargar_datos_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)
        for cliente in bd_c.ver_clientes():
            tabla.insert("", "end", values=cliente)

    def limpiar_campos():
        for e in (entrada_nombre, entrada_apellido, entrada_telefono, entrada_fecha):
            e.config(state="normal")
            e.delete(0, tk.END)
            e.config(bg="#FFFFFF")
        menu_seleccion.set("")
        id_cliente_seleccionado.set("")

    def al_seleccionar_registro(event):
        item = tabla.focus()
        if not item:
            return
        valores = tabla.item(item, "values")
        if not valores:
            return
        id_cliente_seleccionado.set(valores[0])
        for entry, valor in zip(
            (entrada_nombre, entrada_apellido, entrada_telefono, entrada_fecha),
            (valores[1], valores[2], valores[3], valores[5])
        ):
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, valor)
            entry.config(bg="#FFFFFF")
        for entry in (entrada_nombre, entrada_apellido, entrada_fecha):
            entry.config(state="readonly")
        menu_seleccion.set(valores[4])

    tabla.bind("<<TreeviewSelect>>", al_seleccionar_registro)

    # ---- Acciones ----
    def accion_agregar():
        n = entrada_nombre.get().strip()
        a = entrada_apellido.get().strip()
        t = entrada_telefono.get().strip()
        membresia = menu_seleccion.get().strip()
        f = entrada_fecha.get().strip()

        if not (n and a and t and membresia and f):
            messagebox.showwarning("Advertencia", "Completa todos los campos.", parent=ventana)
            return
        if not (n.replace(" ", "").isalpha() and a.replace(" ", "").isalpha()):
            messagebox.showwarning("Advertencia", "Escribe solo letras en nombre y apellido.", parent=ventana)
            return
        if not t.isdigit() or len(t) != 10:
            messagebox.showwarning("Advertencia", "Escribe solo 10 números en Teléfono.", parent=ventana)
            return
        try:
            datetime.strptime(f, "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Advertencia", "Formato de fecha inválido (DD/MM/AAAA).", parent=ventana)
            return
        if not confirmar_accion(ventana):
            return
        try:
            nuevo_id = bd_c.agregar_cliente(n, a, t, membresia, f)
            bam.registrar_estado_inicial(nuevo_id)
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=ventana)
            return
        messagebox.showinfo("Cliente agregado", f"ID asignado: {nuevo_id}", parent=ventana)
        cargar_datos_tabla()
        limpiar_campos()

    def accion_actualizar():
        c_id = id_cliente_seleccionado.get()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un cliente primero.", parent=ventana)
            return

        n = entrada_nombre.get().strip()
        a = entrada_apellido.get().strip()
        t = entrada_telefono.get().strip()
        membresia = menu_seleccion.get().strip()
        f = entrada_fecha.get().strip()

        if not (n and a and t and membresia and f):
            messagebox.showwarning("Advertencia", "Completa todos los campos.", parent=ventana)
            return
        if not (n.replace(" ", "").isalpha() and a.replace(" ", "").isalpha()):
            messagebox.showwarning("Advertencia", "Escribe solo letras en nombre y apellido.", parent=ventana)
            return
        if not t.isdigit() or len(t) != 10:
            messagebox.showwarning("Advertencia", "Escribe solo 10 números en Teléfono.", parent=ventana)
            return
        try:
            datetime.strptime(f, "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning("Advertencia", "Formato de fecha inválido (DD/MM/AAAA).", parent=ventana)
            return
        if not confirmar_accion(ventana):
            return
        try:
            ok = bd_c.modificar_cliente(
                c_id,
                nombre=n,
                apellido=a,
                telefono=t,
                tipo_membresia=membresia,
                fecha_nacimiento=f
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=ventana)
            return
        if not ok:
            messagebox.showerror("Error", "El ID no existe en la base de datos.", parent=ventana)
            return
        cargar_datos_tabla()
        limpiar_campos()

    def accion_eliminar():
        c_id = id_cliente_seleccionado.get()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un cliente primero.", parent=ventana)
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar al cliente {c_id}?", parent=ventana):
            return
        bd_c.eliminar_cliente(c_id)
        bam.eliminar_estado(c_id)
        cargar_datos_tabla()
        limpiar_campos()

    # ---- Botones ----
    crear_boton(panel_para_modificar, 
                "AGREGAR", 
                accion_agregar,
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar, 
                "ACTUALIZAR", 
                accion_actualizar,
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar, 
                "ELIMINAR", 
                accion_eliminar,
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar, 
                "LIMPIAR", 
                lambda: (tabla.selection_remove(tabla.selection()), limpiar_campos()),
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")

    cargar_datos_tabla()


## Ventana Estado Membresía
def Crear_Ventana_Estado_Membresia(ventana_padre):
    ventana_padre.withdraw()
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Estado de Membresía")
    ventana.geometry("1300x700")
    ventana.resizable(False, False)
    ventana.configure(bg=est.COLOR_FONDO)
    ventana.protocol("WM_DELETE_WINDOW", lambda: (ventana_padre.deiconify(), ventana.destroy()))

    # ---- Panel de la tabla (derecha) ----
    panel_tabla = tk.Frame(ventana, bg=est.FONDO_TABLA)
    panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)

    columnas = ("ID", "Nombre", "Apellido", "Membresía", "Inicio", "Vencimiento", "Estado")
    tabla = ttk.Treeview(panel_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=60 if col == "ID" else 120)

    scrollbar = ttk.Scrollbar(panel_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(expand=True, fill="both")

    # ---- Panel para modificar (izquierda) ----
    panel_para_modificar = tk.Frame(ventana, bg=est.COLOR_FONDO, padx=15, pady=15)
    panel_para_modificar.pack(side="left", fill="y")

    tk.Label(panel_para_modificar,
             text="ESTADO DE\nMEMBRESÍA",
             font=est.FUENTE_SUBTITULO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=20).pack(padx=15)

    entrada_id = campo(panel_para_modificar, "ID Cliente:", "texto")
    entrada_fecha_inicio = campo(panel_para_modificar, "Fecha inicio (DD/MM/AAAA):", "fecha")
    entrada_estado = campo(panel_para_modificar, "Estado:", "texto")

    for e in (entrada_id, entrada_fecha_inicio, entrada_estado):
        e.config(state="readonly")

    # ---- Auxiliares ----
    def poner_texto(entry, texto):
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, texto)
        entry.config(state="readonly")

    def cargar_datos_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)
        for cliente in bam.estado_cliente():
            tabla.insert("", "end", values=cliente)

    def limpiar_campos():
        for e in (entrada_id, entrada_fecha_inicio, entrada_estado):
            poner_texto(e, "")

    def seleccionar(event):
        item = tabla.focus()
        if not item:
            return
        valores = tabla.item(item, "values")
        if valores:
            poner_texto(entrada_id, valores[0])
            poner_texto(entrada_fecha_inicio, valores[4])
            poner_texto(entrada_estado, valores[6])

    tabla.bind("<<TreeviewSelect>>", seleccionar)

    # ---- Acciones ----
    def accion_renovar():
        c_id = entrada_id.get().strip()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un registro de la tabla.", parent=ventana)
            return
        if not confirmar_accion(ventana):
            return
        bam.renovar_membresia(c_id)
        cargar_datos_tabla()
        limpiar_campos()

    def accion_desactivar():
        c_id = entrada_id.get().strip()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un registro de la tabla.", parent=ventana)
            return
        if not confirmar_accion(ventana):
            return
        bam.desactivar_membresia(c_id)
        cargar_datos_tabla()
        limpiar_campos()

    # ---- Botones ----
    crear_boton(panel_para_modificar,
                "RENOVAR",
                accion_renovar,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar,
                "DESACTIVAR",
                accion_desactivar,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")

    cargar_datos_tabla()


## Ventana Tipo de Membresía
def Crear_Ventana_Tipo_Membresia(ventana_padre):
    ventana_padre.withdraw()
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Tipos de Membresía")
    ventana.geometry("1300x700")
    ventana.resizable(False, False)
    ventana.configure(bg=est.COLOR_FONDO)
    ventana.protocol("WM_DELETE_WINDOW",
                     lambda: (ventana_padre.deiconify(), ventana.destroy()))

    membresia_seleccionada = tk.StringVar()

    # ---- Panel de la tabla (derecha) ----
    panel_tabla = tk.Frame(ventana, bg=est.FONDO_TABLA)
    panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)

    columnas = ("Membresía", "Precio", "Clientes Inscritos")
    tabla = ttk.Treeview(panel_tabla, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=150)
    tabla.pack(expand=True, fill="both")

    # ---- Panel para modificar (izquierda) ----
    panel_para_modificar = tk.Frame(ventana, bg=est.COLOR_FONDO, padx=15, pady=15)
    panel_para_modificar.pack(side="left", fill="y")

    # ------- Titulo -------
    tk.Label(panel_para_modificar, text="Tipos de Membresía",
             font=est.FUENTE_SUBTITULO, bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO, pady=20).pack(padx=15)

    entrada_nombre = campo(panel_para_modificar, "Nombre:", "texto")
    entrada_precio = campo(panel_para_modificar, "Precio:", "numeros")
    entrada_cant_clientes = campo(panel_para_modificar, "Cantidad Clientes:", "numeros")
    entrada_cant_clientes.config(state="readonly")

    # ---- Funciones Auxiliares ----
    def cargar_datos_tabla():
        for item in tabla.get_children():
            tabla.delete(item)
        for fila in tm.ver_membresia():
            tabla.insert("", "end", values=fila)

    def limpiar_datos():
        for e in (entrada_nombre, entrada_precio):
            e.delete(0, tk.END)
            e.config(bg="#FFFFFF")

        entrada_cant_clientes.config(state="normal")
        entrada_cant_clientes.delete(0, tk.END)
        entrada_cant_clientes.config(state="readonly")

        membresia_seleccionada.set("")

    def al_seleccionar_registro(evento):
        item = tabla.focus()
        if not item:
            return
        valores = tabla.item(item, "values")
        if not valores:
            return
        membresia_seleccionada.set(valores[0])

        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, valores[0])
        entrada_nombre.config(bg="#FFFFFF")

        entrada_precio.delete(0, tk.END)
        entrada_precio.insert(0, valores[1])
        entrada_precio.config(bg="#FFFFFF")

        entrada_cant_clientes.config(state="normal")
        entrada_cant_clientes.delete(0, tk.END)
        entrada_cant_clientes.insert(0, valores[2])
        entrada_cant_clientes.config(state="readonly")

    tabla.bind("<<TreeviewSelect>>", al_seleccionar_registro)

    def accion_agregar():
        nombre = entrada_nombre.get().strip()
        precio = entrada_precio.get().strip()
        if not (nombre and precio):
            return
        try:
            tm.añadir_membresia(nombre, float(precio))
            messagebox.showinfo("Exito", "Membresía agregada", parent=ventana)
            cargar_datos_tabla()
            limpiar_datos()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=ventana)
    
    def accion_actualizar():
        nombre = membresia_seleccionada.get()
        precio = entrada_precio.get().strip()
        if not nombre:
            messagebox.showwarning("Advertencia", "Selecciona una membresía de la tabla", parent=ventana)
            return
        if not precio:
            messagebox.showwarning("Advertencia", "Ingresa el nuevo precio", parent=ventana)
            return
        try:
            tm.modificar_membresia(nombre, precio=float(precio))
            messagebox.showinfo("Exito", "Precio actualizado", parent=ventana)
            cargar_datos_tabla()
            limpiar_datos()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=ventana)

    def accion_eliminar():
        nombre = membresia_seleccionada.get()
        e_cli = entrada_cant_clientes.get().strip()
        if e_cli and int(e_cli) > 0:
            messagebox.showerror("Error", "Esta membresía tiene clientes activos.", parent=ventana)
            return
        if not nombre:
            messagebox.showwarning("Advertencia", "Selecciona una membresía de la tabla", parent=ventana)
            return
        if messagebox.askyesno("Confirmar", f"Estas 100% seguro que deseas eliminar la membresía {nombre}?", parent=ventana):
            tm.eliminar_membresia(nombre)
            cargar_datos_tabla()
            limpiar_datos()

    # ---- Botones ----
    crear_boton(panel_para_modificar, 
                "AGREGAR", 
                accion_agregar,
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar, 
                "Modificar", 
                accion_actualizar,
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar, 
                "ELIMINAR", 
                accion_eliminar,
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")

    cargar_datos_tabla()


## Ventana de Inversión
def Crear_Ventana_Inversion(ventana_padre):
    ventana_padre.withdraw()
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Inversión")
    ventana.geometry("1300x700")
    ventana.resizable(False, False)
    ventana.configure(bg=est.COLOR_FONDO)
    ventana.protocol("WM_DELETE_WINDOW",
                     lambda: (ventana_padre.deiconify(), ventana.destroy()))

    panel_tabla = tk.Frame(ventana, bg=est.FONDO_TABLA)
    panel_tabla.pack(side="top", expand=True, fill="both", padx=15, pady=15)

    columnas = ("Membresía", "Mensual", "Anual")
    tabla = ttk.Treeview(panel_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=150)

    scrollbar = ttk.Scrollbar(panel_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(expand=True, fill="both")


    panel_totales = tk.Frame(ventana, bg=est.COLOR_FONDO)
    panel_totales.pack(side="bottom", fill="x", padx=15, pady=15)


    label_mensual = tk.Label(panel_totales, 
                             text="Ganancia Total Mensual: $0.00", 
                             font=est.FUENTE_SUBTITULO, 
                             bg=est.COLOR_FONDO, 
                             fg=est.COLOR_TEXTO)
    label_mensual.pack(side="left", expand=True)

    label_anual = tk.Label(panel_totales, 
                           text="Ganancia Total Anual: $0.00", 
                           font=est.FUENTE_SUBTITULO, 
                           bg=est.COLOR_FONDO, 
                           fg=est.COLOR_TEXTO)
    label_anual.pack(side="right", expand=True)


    def cargar_datos_tabla():
        
        for fila in tabla.get_children():
            tabla.delete(fila)
            
     
        for fila in tm.ver_ganancias_proyectadas():
            nombre, mensual, anual = fila
            tabla.insert("", "end", values=(nombre, f"${mensual:.2f}", f"${anual:.2f}"))
            
   
        total_m, total_a = tm.ver_ganancias_totales()
        label_mensual.config(text=f"Ganancia Total Mensual: ${total_m:.2f}")
        label_anual.config(text=f"Ganancia Total Anual: ${total_a:.2f}")

    cargar_datos_tabla()

## Ventana Empleados
def Crear_Ventana_Empleados(ventana_padre):
    ventana_padre.withdraw()
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Empleados")
    ventana.geometry("1300x700")
    ventana.resizable(False, False)
    ventana.configure(bg=est.COLOR_FONDO)
    ventana.protocol("WM_DELETE_WINDOW",
                     lambda: (ventana_padre.deiconify(), ventana.destroy()))

    id_empleado_seleccionado = tk.StringVar()

    # ---- Panel de la tabla (derecha) ----
    panel_tabla = tk.Frame(ventana, bg=est.FONDO_TABLA)
    panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)

    columnas = ("ID", "Nombre", "Apellido", "Teléfono", "Contraseña")
    tabla = ttk.Treeview(panel_tabla, columns=columnas, show="headings")

    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=130)

    scrollbar = ttk.Scrollbar(panel_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(expand=True, fill="both")

    # ---- Panel para modificar (izquierda) ----
    panel_para_modificar = tk.Frame(ventana, bg=est.COLOR_FONDO, padx=15, pady=15)
    panel_para_modificar.pack(side="left", fill="y")

    tk.Label(panel_para_modificar,
             text="EMPLEADOS",
             font=est.FUENTE_SUBTITULO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=20).pack(padx=15)

    entrada_nombre = campo(panel_para_modificar, "Nombre:", "texto")
    entrada_apellido = campo(panel_para_modificar, "Apellido:", "texto")
    entrada_telefono = campo(panel_para_modificar, "Teléfono:", "telefono")
    entrada_puesto = campo(panel_para_modificar, "Contraseña:", "texto")

    # ---- Auxiliares ----
    def cargar_datos_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)
        # Conectar BD aquí

    def limpiar_campos():
        for e in (entrada_nombre, entrada_apellido, entrada_telefono, entrada_puesto):
            e.delete(0, tk.END)
        id_empleado_seleccionado.set("")

    def al_seleccionar_registro(event):
        item = tabla.focus()
        if not item:
            return
        valores = tabla.item(item, "values")
        if not valores:
            return
        id_empleado_seleccionado.set(valores[0])
        for entry, valor in zip(
            (entrada_nombre, entrada_apellido, entrada_telefono, entrada_puesto),
            valores[1:]
        ):
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    tabla.bind("<<TreeviewSelect>>", al_seleccionar_registro)

    # ---- Acciones ----
    def accion_agregar():
        pass

    def accion_actualizar():
        pass

    def accion_eliminar():
        pass

    # ---- Botones ----
    crear_boton(panel_para_modificar,
                "AGREGAR",
                accion_agregar,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar,
                "ACTUALIZAR",
                accion_actualizar,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar,
                "ELIMINAR",
                accion_eliminar,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")

    cargar_datos_tabla()