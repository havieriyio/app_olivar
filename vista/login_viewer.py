import tkinter as tk
from tkinter import messagebox
from modelo.acceso_usuario import verificar_credenciales

class LoginViewer(tk.Tk):
    def __init__(self, callback_login_exitoso):
        super().__init__()
        self.title("Iniciar sesión")

        self.callback_login_exitoso = callback_login_exitoso

        tk.Label(self, text="Usuario:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)

        self.usuario_entry = tk.Entry(self)
        self.contrasena_entry = tk.Entry(self, show="*")

        self.usuario_entry.grid(row=0, column=1)
        self.contrasena_entry.grid(row=1, column=1)

        tk.Button(self, text="Entrar", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()
        resultado = verificar_credenciales(usuario, contrasena)

        if resultado:
            self.destroy()
            self.callback_login_exitoso(resultado)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
