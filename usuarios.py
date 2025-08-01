import tkinter as tk
from tkinter import messagebox
import sqlite3

# Crear la base de datos y tabla si no existen
conexion = sqlite3.connect("usuarios.db")
cursor = conexion.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT NOT NULL,
        tipo_documento TEXT NOT NULL,
        numero_documento TEXT NOT NULL UNIQUE,
        correo TEXT NOT NULL,
        celular TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        contraseña TEXT NOT NULL
    )
''')
conexion.commit()
conexion.close()

# Función para registrar el usuario
def registrar_usuario():
    datos = {
        "nombre": entrada_nombre.get(),
        "tipo_doc": entrada_tipo_documento.get(),
        "numero_doc": entrada_numero_documento.get(),
        "correo": entrada_correo.get(),
        "celular": entrada_celular.get(),
        "usuario": entrada_usuario.get(),
        "contraseña": entrada_contraseña.get()
    }

    if not all(datos.values()):
        messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
        return

    conexion = sqlite3.connect("usuarios.db")
    cursor = conexion.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (nombre_completo, tipo_documento, numero_documento, correo, celular, usuario, contraseña) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (datos["nombre"], datos["tipo_doc"], datos["numero_doc"], datos["correo"], datos["celular"], datos["usuario"], datos["contraseña"]))
        conexion.commit()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: usuarios.usuario" in str(e):
            messagebox.showerror("Error", "El nombre de usuario ya está en uso.")
        elif "UNIQUE constraint failed: usuarios.numero_documento" in str(e):
            messagebox.showerror("Error", "El número de documento ya está registrado.")
        else:
            messagebox.showerror("Error", str(e))
    finally:
        conexion.close()

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Registro de Usuario")
ventana.geometry("400x400")

tk.Label(ventana, text="Nombre completo:").pack()
entrada_nombre = tk.Entry(ventana)
entrada_nombre.pack()

tk.Label(ventana, text="Tipo de documento:").pack()
entrada_tipo_documento = tk.Entry(ventana)
entrada_tipo_documento.pack()

tk.Label(ventana, text="Número de documento:").pack()
entrada_numero_documento = tk.Entry(ventana)
entrada_numero_documento.pack()

tk.Label(ventana, text="Correo:").pack()
entrada_correo = tk.Entry(ventana)
entrada_correo.pack()

tk.Label(ventana, text="Celular:").pack()
entrada_celular = tk.Entry(ventana)
entrada_celular.pack()

tk.Label(ventana, text="Usuario:").pack()
entrada_usuario = tk.Entry(ventana)
entrada_usuario.pack()

tk.Label(ventana, text="Contraseña:").pack()
entrada_contraseña = tk.Entry(ventana, show="*")
entrada_contraseña.pack()

tk.Button(ventana, text="Registrar", command=registrar_usuario).pack(pady=15)

ventana.mainloop()


