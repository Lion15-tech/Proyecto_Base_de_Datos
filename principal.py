import tkinter as tk
import estilos as est  
import funciones as func
import os
#From estilos import *

#import base datos
#import funciones

def crear_ventana_principal():
    func.inicializar_tablas()
    ventana_principal = tk.Tk()
    ventana_principal.title("Base de Datos")
    ventana_principal.resizable(False, False)
    ventana_principal.geometry("500x650")
    ventana_principal.config(bg=est.COLOR_FONDO)
    ## CONFIGURACIÓN DEL ICONO ##
    carpeta_proyecto = os.path.dirname(__file__)
    ruta_icono = os.path.join(carpeta_proyecto, "logo_cecyteq.png")
    try:
        icono = tk.PhotoImage(file=ruta_icono)
        ventana_principal.iconphoto(True, icono)
    except Exception as e:
        print(f"Error al cargar el icono: {e}")

    #----- TITULO ----

    tk.Label(
        ventana_principal,
        text="BASE DE DATOS",
        font=est.FUENTE_TITULO,
        bg=est.COLOR_FONDO,
        fg=est.COLOR_TEXTO,
        pady=20
    ).pack()    


    # ====== BOTONES ======

    # ----- Clientes -----
    func.crear_boton(
        ventana_principal, 
        "Clientes", 
        lambda: func.Crear_Ventana_Clientes(ventana_principal), 
        est.FUENTE_TEXTO,
        est.COLOR_BOTON, 
        est.COLOR_TEXTO, 
        est.COLOR_BOTON_EFECTO).pack(padx=50, pady=20, fill="both")

    # ---- Estado de Membresía ----
    func.crear_boton(
        ventana_principal, 
        "Estado de membresía", 
        lambda: func.Crear_Ventana_Estado_Membresia(ventana_principal), 
        est.FUENTE_TEXTO,
        est.COLOR_BOTON, 
        est.COLOR_TEXTO, 
        est.COLOR_BOTON_EFECTO).pack(padx=50, pady=20, fill="both")

    # ---- Tipo de Membresía ----
    func.crear_boton(
        ventana_principal, 
        "Tipo de Membresía",
        lambda: func.Crear_Ventana_Tipo_Membresia(ventana_principal), 
        est.FUENTE_TEXTO,
        est.COLOR_BOTON, 
        est.COLOR_TEXTO, 
        est.COLOR_BOTON_EFECTO).pack(padx=50, pady=20, fill="both")

    # ---- Inversión ----
    func.crear_boton(
        ventana_principal, 
        "Ganancias", 
        lambda: func.Crear_Ventana_Inversion(ventana_principal), 
        est.FUENTE_TEXTO,
        est.COLOR_BOTON, 
        est.COLOR_TEXTO, 
        est.COLOR_BOTON_EFECTO).pack(padx=50, pady=20, fill="both")

    # ----- Empleados/Admins ----
    func.crear_boton(
        ventana_principal, 
        "Gerentes", 
        lambda: func.Crear_Ventana_Empleados(ventana_principal), 
        est.FUENTE_TEXTO,
        est.COLOR_BOTON, 
        est.COLOR_TEXTO, 
        est.COLOR_BOTON_EFECTO).pack(padx=50, pady=20, fill="both")

    ventana_principal.mainloop()


if __name__ == "__main__":
    crear_ventana_principal()

#HORAS GASTADAS: 27

#poner .lower para tipo membresia y hacer un if para solo admitir las membresias que esten en la tabla de membresia
#poner nacimiento tipo dinamico 3 cuadros modificar .get y la otra cosa
"""
Errores encontrados:
    {estesticos}
    falta resizable false

    {mecanicos}
    no se puede actualizar la membresia si el usuario tiene una membresia que no hay
    Rodrigo: supongo que eso ya quedó solucionado cuando borraste toda la BD y creaste una nueva donde 
    ahorita solo permite el colocar las del comobobox, no?
    
    {messagebox}
    se puede spamear message box (por alguna razon permite seguir dando clic execpto en la ventana madre)
    Rodrigo: me salio un error muy curioso al estar viendo que onda en linux jajaja no se si es por i3wm o algo
    más, pero salió esto:
        '󰣇 lionx in ~/Proyectos/Proyecto_Base_de_Datos on  main ❯ python principal.py 
         Exception in Tkinter callback
         Traceback (most recent call last):
           File "/usr/lib/python3.14/tkinter/__init__.py", line 2114, in __call__
             return self.func(*args)
                    ~~~~~~~~~^^^^^^^
           File "/home/lionx/Proyectos/Proyecto_Base_de_Datos/funciones.py", line 264, in <lambda>
             lambda: (accion_actualizar()),
                      ~~~~~~~~~~~~~~~~~^^
           File "/home/lionx/Proyectos/Proyecto_Base_de_Datos/funciones.py", line 207, in accion_actualizar
             messagebox.showwarning("Advertencia", "Selecciona un cliente primero.")
             ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
           File "/usr/lib/python3.14/tkinter/messagebox.py", line 95, in showwarning
             return _show(title, message, WARNING, OK, **options)
           File "/usr/lib/python3.14/tkinter/messagebox.py", line 78, in _show
             res = Message(**options).show()
           File "/usr/lib/python3.14/tkinter/commondialog.py", line 47, in show
             s = master.tk.call(self.command, *master._options(self.options))
         _tkinter.TclError: can't invoke "grab" command: application has been destroyed'
    Mañana lo reviso en la compu de la escuela

    creo que seria mejor si en vez de tanto mesasgebox al dar error fuera un disable en los botones
    el inconveniente es que ek usuario debe revisar manualmente cuales su error
    Rodrigo: esto lo podemos debatir mañana para ver que combiene más
    
    ERROR DE CANTIDAD DE NUMEROS EN EL ENTRY DE TELEFONO SOLUCIONADO
"""