import tkinter as tk
from tkinter import messagebox
import estilos as est
import funciones as func
import principal
import os

def login():
    ventana_login = tk.Tk()
    ventana_login.title("Login Base de Datos")
    ventana_login.resizable(False, False)
    ventana_login.geometry("400x600")
    ventana_login.config(bg=est.COLOR_FONDO)
    ## CONFIGURACIÓN DEL ICONO ##
    carpeta_proyecto = os.path.dirname(__file__)
    ruta_icono = os.path.join(carpeta_proyecto, "logo_cecyteq.png")
    try:
        icono = tk.PhotoImage(file=ruta_icono)
        ventana_login.iconphoto(True, icono)
    except Exception as e:
        print(f"Error al cargar el icono: {e}")

    tk.Label(ventana_login,
             text="LOGIN",
             font=est.FUENTE_TITULO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=20
         ).pack()

    tk.Label(ventana_login,
             text="Usuario",
             font=est.FUENTE_SUBTITULO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=20
         ).pack(padx=15,)
    user = tk.Entry(ventana_login,
                    justify="center")
    user.pack(padx=15, pady=20)

    tk.Label(ventana_login,
             text="Contraseña",
             font=est.FUENTE_SUBTITULO,
             bg=est.COLOR_FONDO,
             fg=est.COLOR_TEXTO,
             pady=20
         ).pack(padx=15)
    password = tk.Entry(ventana_login,
                          justify="center",
                          show="*")
    password.pack(padx=15, pady=20,)

    def validar_login():
        usuario = user.get().strip()
        contraseña = password.get().strip()

        # Aquí hay que cambiarle para que valide con respecto a la base de datos de Empleados
        if usuario == "Admin" and contraseña == "1234":
            ventana_login.destroy()
            principal.crear_ventana_principal()
        else:
            messagebox.showerror("Error", "El usuario o contraseña son incorrectos")

    func.crear_boton(ventana_login,
                     "Iniciar Sesión",
                     validar_login,
                     est.FUENTE_BOTONES,
                     est.COLOR_BOTON,
                     est.COLOR_TEXTO,
                     est.COLOR_BOTON_EFECTO).pack(padx=15, pady=20)

    ventana_login.mainloop()



# --- Para probar que funcione --- #
if __name__ == "__main__":
    login()