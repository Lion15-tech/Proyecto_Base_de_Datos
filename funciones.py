import tkinter as tk
from tkinter import ttk, messagebox
import estilos as est
import bd_Clientes as bd
from datetime import datetime
import bd_tipos_membresia as tm

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

def crear_boton(padre, texto, comando, fuente_texto,color_fondo, color_texto, color_boton_presionado):
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


# Etiqueta + entry
def campo(panel_form, etiqueta, tipo_validacion):
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
    entrada_telefono = campo(panel_para_modificar, "Teléfono:", "numeros")

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
        for cliente in bd.ver_clientes():
            tabla.insert("", "end", values=cliente)

    def limpiar_campos():
        for e in (entrada_nombre, entrada_apellido, entrada_telefono,
                  entrada_fecha):
            e.delete(0, tk.END)
        id_cliente_seleccionado.set("")

    def al_seleccionar_registro(event): #no muevas esto
        item = tabla.focus()
        if not item:
            return
        valores = tabla.item(item, "values")
        if not valores:
            return
        id_cliente_seleccionado.set(valores[0])
        for entry, valor in zip(
            (entrada_nombre, entrada_apellido, entrada_telefono,
             menu_seleccion, entrada_fecha),
            valores[1:]
        ):
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    tabla.bind("<<TreeviewSelect>>", al_seleccionar_registro)

    # ---- Acciones ----
    def accion_agregar():
        n  = entrada_nombre.get().strip()
        a  = entrada_apellido.get().strip()
        t  = entrada_telefono.get().strip()
        membresia = menu_seleccion.get().strip()
        f  = entrada_fecha.get().strip()

        if not (n and a and t and membresia and f): # Tu codigo es basura   ATTE: Jared
            messagebox.showwarning("Advertencia", "Completa todos los campos.", parent=ventana)
            return
        if not (n or a).replace(" ", "").isalpha():
            return
        if not t.isdigit() or len(t) != 10:
            return
        if not confirmar_accion():
            return
        try:
            nuevo_id = bd.agregar_cliente(n, a, t, membresia, f)
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

        n  = entrada_nombre.get().strip()
        a  = entrada_apellido.get().strip()
        t  = entrada_telefono.get().strip()
        membresia = menu_seleccion.get().strip()
        f  = entrada_fecha.get().strip()

        if not (n and a and t and membresia and f):
            messagebox.showwarning("Advertencia", "Completa todos los campos.", parent=ventana)
            return
        if not (n or a).isalpha():
            return
        if not t.isdigit() or len(t) != 10:
            return
        if not confirmar_accion():
            return
        try:
            ok = bd.modificar_cliente(
                c_id,
                nombre=entrada_nombre.get().strip(),
                apellido=entrada_apellido.get().strip(),
                telefono=entrada_telefono.get().strip(),
                tipo_membresia=menu_seleccion.get().strip(),
                fecha_nacimiento=entrada_fecha.get().strip()
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
        bd.eliminar_cliente(c_id)
        cargar_datos_tabla()
        limpiar_campos()

    # ---- Botones ----
    crear_boton(panel_para_modificar, 
                "AGREGAR", 
                lambda: (accion_agregar()),
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar, 
                "ACTUALIZAR", 
                lambda: (accion_actualizar()),
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar, 
                "ELIMINAR", 
                lambda: (accion_eliminar()),
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")

    cargar_datos_tabla()


def Crear_Ventana_Estado_Membresia(ventana_padre):
    ventana_padre.withdraw()
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Estado de Membresía")
    ventana.geometry("1000x600")
    ventana.configure(bg=est.COLOR_FONDO)
    # Si el usuario cierra la ventana regresa al menu inicial
    ventana.protocol("WM_DELETE_WINDOW", lambda:(ventana_padre.deiconify(), ventana.destroy())) 

    # -- Variable para rastrear el id del cliente -- #
    id_cliente_seleccionado = tk.StringVar()
    
    # Creamos el Frame donde ingresar los datos
    panel_para_modificar = tk.Frame(ventana,
                            bg=est.COLOR_FONDO,
                            padx=15,
                            pady=15)
    panel_para_modificar.pack(side="left", fill="y")
    # Creamos el Frame para la tabla
    panel_tabla = tk.Frame(ventana,
                            bg=est.FONDO_TABLA)
    panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)
    # ------ Titulo ------
    tk.Label(panel_para_modificar,
            text="ESTADO DE \nMEMBRESÍA",
            font=est.FUENTE_SUBTITULO,
            bg=est.COLOR_FONDO,
            fg=est.COLOR_TEXTO,
            pady=20
            ).pack(padx=15)
    # Entrys
    tk.Label(panel_para_modificar,
                     text="Tipo de Membresía:",
                     font=est.FUENTE_TEXTO,
                     bg=est.COLOR_FONDO,
                     fg=est.COLOR_TEXTO,
                     pady=5).pack(padx=5)
    tipo_membresia = tk.Entry(panel_para_modificar,
                    justify="center")
    tipo_membresia.pack(padx=15, pady=15)
    tk.Label(panel_para_modificar,
                             text="Vigencia:",
                             font=est.FUENTE_TEXTO,
                             bg=est.COLOR_FONDO,
                             fg=est.COLOR_TEXTO,
                             pady=5).pack(padx=5)
    vigencia = tk.Entry(panel_para_modificar,
                    justify="center")
    vigencia.pack(padx=15, pady=15)
    tk.Label(panel_para_modificar,
                             text="Fecha de Pago:",
                             font=est.FUENTE_TEXTO,
                             bg=est.COLOR_FONDO,
                             fg=est.COLOR_TEXTO,
                             pady=5).pack(padx=5)
    fecha_prox_pago = tk.Entry(panel_para_modificar,
                    justify="center")
    fecha_prox_pago.pack(padx=15, pady=15)
    ## --- Botones --- ##
    # Agregar
    crear_boton(panel_para_modificar,
                "AGREGAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10, fill="both")
    # Actualizar 
    crear_boton(panel_para_modificar,
                "ACTUALIZAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10, fill="both")
    # Eliminar
    crear_boton(panel_para_modificar,
                "ELIMINAR",
                lambda: None,
                est.FUENTE_BOTONES,
                est.COLOR_BOTON,
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=10, fill="both")
             
    # --- Widget Treeview (Tabla) ---
    columnas = ("ID", "Tipo de Membresía", "Vigencia", "Fecha de próximo pago")
    tabla = ttk.Treeview(panel_tabla, columns=columnas, show="headings")
    
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=120)
    
    # Agregar Scrollbar a la tabla
    scrollbar = ttk.Scrollbar(panel_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabla.pack(expand=True, fill="both")
    
    # --- Funciones Auxiliares para la Interfaz ---
    def cargar_datos_tabla():
        for fila in tabla.get_children():
            tabla.delete(fila)
        for cliente in bd.obtener_clientes():
            tabla.insert("", "end", values=cliente)
    
    def limpiar_campos():
        tipo_membresia.delete(0, tk.END)
        vigencia.delete(0, tk.END)
        fecha_prox_pago.delete(0, tk.END)
        id_cliente_seleccionado.set("")
    
    def al_seleccionar_registro(event):
        item_seleccionado = tabla.focus()
        if not item_seleccionado:
            return
        valores = tabla.item(item_seleccionado, "values")
        if valores:
            id_cliente_seleccionado.set(valores[0])
            
            tipo_membresia.delete(0, tk.END)
            tipo_membresia.insert(0, valores[1])
            
            vigencia.delete(0, tk.END)
            vigencia.insert(0, valores[2])
            
            fecha_prox_pago.delete(0, tk.END)
            fecha_prox_pago.insert(0, valores[3])
    
    # Enlazar la selección en la tabla con la función de autollenado
    tabla.bind("<<TreeviewSelect>>", al_seleccionar_registro)
    
    # --- Acciones de Botones ---
    def accion_agregar():
        n, a, t = tipo_membresia.get(), vigencia.get(), fecha_prox_pago.get()
        if n and a and t:
            bd.agregar_cliente(n, a, t)
            cargar_datos_tabla()
            limpiar_campos()
        else:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos.")
    
    def accion_actualizar():
        c_id = id_cliente_seleccionado.get()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un usuario de la tabla para modificar.")
            return
        n, a, t = tipo_membresia.get(), vigencia.get(), fecha_prox_pago.get()
        bd.actualizar_cliente(c_id, n, a, t)
        cargar_datos_tabla()
        limpiar_campos()
    
    def accion_eliminar():
        c_id = id_cliente_seleccionado.get()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un usuario de la tabla para eliminar.")
            return
        bd.eliminar_cliente(c_id)
        cargar_datos_tabla()
        limpiar_campos()
    # Carga inicial de registros
    cargar_datos_tabla()


def Crear_Ventana_Tipo_Membresia(ventana_padre):
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

    # ------- Titulo -------
    tk.Label(panel_para_modificar, text="Tipos de Membresía",
             font=est.FUENTE_SUBTITULO, bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO, pady=20).pack(padx=15)
    
    membresias = ["Beneficios", "Planes"]
    menu_seleccion = ttk.Combobox(panel_para_modificar,
                                  values=membresias,
                                  state="readonly")
    menu_seleccion.set("Beneficios")
    menu_seleccion.pack(pady=10)

    # Entrys
    entrada_nombre = campo(panel_para_modificar, "Nombre:", "texto")
    entrada_apellido = campo(panel_para_modificar, "Apellido:", "texto")
    entrada_telefono = campo(panel_para_modificar, "Teléfono:", "numeros")
    entrada_fecha = campo(panel_para_modificar, "Fecha nacimiento (DD/MM/AAAA):", "fecha")


    # ---- Treeview con 6 columnas ----
    columnas = ("Nombe", "Precio", "Cantidad Clientes")
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
        for cliente in bd.ver_clientes():
            tabla.insert("", "end", values=cliente)

    def limpiar_campos():
        for e in (entrada_nombre, entrada_apellido, entrada_telefono,
                  entrada_fecha):
            e.delete(0, tk.END)
        id_cliente_seleccionado.set("")

    def al_seleccionar_registro(event): #no muevas esto
        item = tabla.focus()
        if not item:
            return
        valores = tabla.item(item, "values")
        if not valores:
            return
        id_cliente_seleccionado.set(valores[0])
        for entry, valor in zip(
            (entrada_nombre, entrada_apellido, entrada_telefono,
             menu_seleccion, entrada_fecha),
            valores[1:]
        ):
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    tabla.bind("<<TreeviewSelect>>", al_seleccionar_registro)

    # ---- Acciones ----
    def accion_agregar():
        n  = entrada_nombre.get().strip()
        a  = entrada_apellido.get().strip()
        t  = entrada_telefono.get().strip()
        membresia = menu_seleccion.get().strip()
        f  = entrada_fecha.get().strip()

        if not (n and a and t and membresia and f): # Tu codigo es basura   ATTE: Jared
            messagebox.showwarning("Advertencia", "Completa todos los campos.", parent=ventana)
            return
        if not (n or a).replace(" ", "").isalpha():
            return
        if not t.isdigit() or len(t) != 10:
            return
        if not confirmar_accion():
            return
        try:
            nuevo_id = bd.agregar_cliente(n, a, t, membresia, f)
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

        n  = entrada_nombre.get().strip()
        a  = entrada_apellido.get().strip()
        t  = entrada_telefono.get().strip()
        membresia = menu_seleccion.get().strip()
        f  = entrada_fecha.get().strip()

        if not (n and a and t and membresia and f):
            messagebox.showwarning("Advertencia", "Completa todos los campos.", parent=ventana)
            return
        if not (n or a).isalpha():
            return
        if not t.isdigit() or len(t) != 10:
            return
        if not confirmar_accion():
            return
        try:
            ok = bd.modificar_cliente(
                c_id,
                nombre=entrada_nombre.get().strip(),
                apellido=entrada_apellido.get().strip(),
                telefono=entrada_telefono.get().strip(),
                tipo_membresia=menu_seleccion.get().strip(),
                fecha_nacimiento=entrada_fecha.get().strip()
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
        bd.eliminar_cliente(c_id)
        cargar_datos_tabla()
        limpiar_campos()

    # ---- Botones ----
    crear_boton(panel_para_modificar, 
                "AGREGAR", 
                lambda: (accion_agregar()),
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar, 
                "ACTUALIZAR", 
                lambda: (accion_actualizar()),
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar, 
                "ELIMINAR", 
                lambda: (accion_eliminar()),
                est.FUENTE_BOTONES, 
                est.COLOR_BOTON, 
                est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")

    cargar_datos_tabla()


def Crear_Ventana_Inversion(ventana_padre):
        ventana_padre.withdraw()
        ventana = tk.Toplevel(ventana_padre)
        ventana.title("Inversión")
        ventana.geometry("1000x600")
        ventana.configure(bg=est.COLOR_FONDO)
        # Si el usuario cierra la ventana regresa al menu inicial
        ventana.protocol("WM_DELETE_WINDOW", lambda:(ventana_padre.deiconify(), ventana.destroy())) 
        
        # Creamos el Frame donde ingresar los datos
        panel_para_modificar = tk.Frame(ventana,
                                bg=est.COLOR_FONDO,
                                padx=15,
                                pady=15)
        panel_para_modificar.pack(side="left", fill="y")
        # Creamos el Frame para la tabla
        panel_tabla = tk.Frame(ventana,
                                bg=est.FONDO_TABLA)
        panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)

        # ------ Titulo -----
        tk.Label(panel_para_modificar,
                text="INVERSIÓN",
                font=est.FUENTE_SUBTITULO,
                bg=est.COLOR_FONDO,
                fg=est.COLOR_TEXTO,
                pady=20
                ).pack(padx=15)
        
        # --- ComboBox para el menú desplegable ---
        # Lista para el combobox
        opciones = ["Costos", "Zonas"]
        menu_seleccion = ttk.Combobox(panel_para_modificar,
                     values=opciones,
                     state="readonly")
        menu_seleccion.pack(pady=10)
        
        # Frames donde se guardan los Entrys
        entrys_Zonas = tk.Frame(panel_para_modificar,
                                bg=est.COLOR_FONDO,
                                padx=15,
                                pady=5)
        tk.Label(entrys_Zonas,
                 text="Precio:",
                 font=est.FUENTE_TEXTO,
                 bg=est.COLOR_FONDO,
                 fg=est.COLOR_TEXTO,
                 pady=5).pack(padx=5)
        nombre_zona = tk.Entry(entrys_Zonas,
                        justify="center")
        nombre_zona.pack(padx=15, pady=15)

        entrys_Costos = tk.Frame(panel_para_modificar,
                                 bg=est.COLOR_FONDO,
                                 padx=15,
                                 pady=5)
        tk.Label(entrys_Costos,
                 text="Precio:",
                 font=est.FUENTE_TEXTO,
                 bg=est.COLOR_FONDO,
                 fg=est.COLOR_TEXTO,
                 pady=5).pack(padx=5)
        costo_unico = tk.Entry(entrys_Zonas,
                        justify="center")
        costo_unico.pack(padx=15, pady=15)


def Crear_Ventana_Instalaciones(ventana_padre):
        ventana_padre.withdraw()
        ventana = tk.Toplevel(ventana_padre)
        ventana.title("Instalaciones")
        ventana.geometry("1000x600")
        ventana.configure(bg=est.COLOR_FONDO)
        # Si el usuario cierra la ventana regresa al menu inicial
        ventana.protocol("WM_DELETE_WINDOW", lambda:(ventana_padre.deiconify(), ventana.destroy())) 
        
        # Creamos el Frame donde ingresar los datos
        panel_para_modificar = tk.Frame(ventana,
                                bg=est.COLOR_FONDO,
                                padx=15,
                                pady=15)
        panel_para_modificar.pack(side="left", fill="y")
        # Creamos el Frame para la tabla
        panel_tabla = tk.Frame(ventana,
                                bg=est.FONDO_TABLA)
        panel_tabla.pack(side="right", expand=True, fill="both", padx=15, pady=15)

        tk.Label(panel_para_modificar,
                text="INSTALACIONES",
                font=est.FUENTE_SUBTITULO,
                bg=est.COLOR_FONDO,
                fg=est.COLOR_TEXTO,
                pady=20
                ).pack(padx=15)
        # Entrys
        nombre = tk.Entry(panel_para_modificar,
                        justify="center")
        nombre.pack(padx=15, pady=15)

        apellido = tk.Entry(panel_para_modificar,
                        justify="center")
        apellido.pack(padx=15, pady=15)
        
        tipo_membresia = tk.Entry(panel_para_modificar,
                        justify="center")
        tipo_membresia.pack(padx=15, pady=15)

        telefono = tk.Entry(panel_para_modificar,
                        justify="center")
        telefono.pack(padx=15, pady=15)


## SE NECESITA MODIFICAR ESTO PORQUE ES UNA COPIA DE CREAR_VENTANA_CLIENTES
def Crear_Ventana_Empleados(ventana_padre):
    ventana_padre.withdraw()
    ventana = tk.Toplevel(ventana_padre)
    ventana.title("Empleados")
    ventana.geometry("1300x700")
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

    tk.Label(panel_para_modificar, text="Empleados",
             font=est.FUENTE_SUBTITULO, bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO, pady=20).pack(padx=15)



    entrada_nombre    = campo("Nombre:")
    entrada_apellido  = campo("Apellido:")
    entrada_telefono  = campo("Teléfono:")
    entrada_membresia = campo("Tipo de membresía:")
    entrada_fecha     = campo("Fecha nacimiento (DDMMAAAA):")

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
        for cliente in bd.ver_clientes():
            tabla.insert("", "end", values=cliente)

    def limpiar_campos():
        for e in (entrada_nombre, entrada_apellido, entrada_telefono,
                  entrada_membresia, entrada_fecha):
            e.delete(0, tk.END)
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
            (entrada_nombre, entrada_apellido, entrada_telefono,
             entrada_membresia, entrada_fecha),
            valores[1:]
        ):
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    tabla.bind("<<TreeviewSelect>>", al_seleccionar_registro)

    # ---- Acciones ----
    def accion_agregar():
        n  = entrada_nombre.get().strip()
        a  = entrada_apellido.get().strip()
        t  = entrada_telefono.get().strip()
        tm = entrada_membresia.get().strip()
        f  = entrada_fecha.get().strip()

        if not (n and a and t and tm and f):
            messagebox.showwarning("Advertencia", "Completa todos los campos.")
            return
        try:
            nuevo_id = bd.agregar_cliente(n, a, t, tm, f)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Cliente agregado", f"ID asignado: {nuevo_id}")
        cargar_datos_tabla()
        limpiar_campos()

    def accion_actualizar():
        c_id = id_cliente_seleccionado.get()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un cliente primero.")
            return
        try:
            ok = bd.modificar_cliente(
                c_id,
                nombre=entrada_nombre.get().strip(),
                apellido=entrada_apellido.get().strip(),
                telefono=entrada_telefono.get().strip(),
                tipo_membresia=entrada_membresia.get().strip(),
                fecha_nacimiento=entrada_fecha.get().strip()
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        if not ok:
            messagebox.showerror("Error", "El ID no existe en la base de datos.")
            return
        cargar_datos_tabla()
        limpiar_campos()

    def accion_eliminar():
        c_id = id_cliente_seleccionado.get()
        if not c_id:
            messagebox.showwarning("Advertencia", "Selecciona un cliente primero.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar al cliente {c_id}?"):
            return
        bd.eliminar_cliente(c_id)
        cargar_datos_tabla()
        limpiar_campos()

    # ---- Botones ----
    crear_boton(panel_para_modificar, "AGREGAR", accion_agregar,
                est.FUENTE_BOTONES, est.COLOR_BOTON, est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar, "ACTUALIZAR", accion_actualizar,
                est.FUENTE_BOTONES, est.COLOR_BOTON, est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")
    crear_boton(panel_para_modificar, "ELIMINAR", accion_eliminar,
                est.FUENTE_BOTONES, est.COLOR_BOTON, est.COLOR_TEXTO,
                est.COLOR_BOTON_EFECTO).pack(padx=15, pady=8, fill="both")

    cargar_datos_tabla()

