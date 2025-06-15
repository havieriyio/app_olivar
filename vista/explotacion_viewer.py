import tkinter as tk
from tkinter import messagebox
from modelo import acceso_explotacion as modelo
from modelo.acceso_explotacion import obtener_explotacion_activa
from modelo.acceso_parcelas import obtener_parcelas_por_explotacion

class ExplotacionViewer:
    def __init__(self, parent):
        self.win = tk.Toplevel(parent)
        self.principal = parent
        self.win.title("Gestión de Explotaciones")
        
        self.frame_lista = tk.Frame(self.win)
        self.frame_lista.pack(padx=10, pady=10)

        self.lista = tk.Listbox(self.frame_lista, width=50)
        self.lista.pack(side=tk.LEFT)

        self.scroll = tk.Scrollbar(self.frame_lista, command=self.lista.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista.config(yscrollcommand=self.scroll.set)

        self.frame_botones = tk.Frame(self.win)
        self.frame_botones.pack(pady=10)

        tk.Button(self.frame_botones, text="Añadir", command=self.anadir).grid(row=0, column=0, padx=5)
        tk.Button(self.frame_botones, text="Eliminar", command=self.eliminar).grid(row=0, column=1, padx=5)
        tk.Button(self.frame_botones, text="Activar", command=self.activar).grid(row=0, column=2, padx=5)
        
        
        self.recargar()

    def recargar(self):
        self.lista.delete(0, tk.END)
        for e in modelo.obtener_todas_explotaciones():
            estado = " (activa)" if e[3] else ""
            self.lista.insert(tk.END, f"{e[0]} - {e[1]} ({e[2]}){estado}")

    def anadir(self):
        top = tk.Toplevel(self.win)
        top.title("Nueva Explotación")

        tk.Label(top, text="Nombre").grid(row=0, column=0)
        nombre = tk.Entry(top)
        nombre.grid(row=0, column=1)

        tk.Label(top, text="Ubicación").grid(row=1, column=0)
        ubicacion = tk.Entry(top)
        ubicacion.grid(row=1, column=1)

        def guardar():
            if nombre.get():
                modelo.insertar_explotacion(nombre.get(), ubicacion.get())
                top.destroy()
                self.recargar()
            else:
                messagebox.showwarning("Faltan datos", "Debe introducir al menos el nombre.")

        tk.Button(top, text="Guardar", command=guardar).grid(row=2, column=0, columnspan=2, pady=5)

    def eliminar(self):
        seleccion = self.lista.curselection()
        if seleccion:
            texto = self.lista.get(seleccion)
            id_explotacion = int(texto.split(" - ")[0])
            modelo.eliminar_explotacion(id_explotacion)
            self.recargar()

    def activar(self):
        seleccion = self.lista.curselection()
        if seleccion:
            texto = self.lista.get(seleccion)
            id_explotacion = int(texto.split(" - ")[0])
            modelo.establecer_explotacion_activa(id_explotacion)
            
        if self.principal and hasattr(self.principal, "actualizar_encabezado"):
            self.principal.actualizar_encabezado()

            self.recargar()

    def seleccionar_explotacion(self, id_explotacion):
        # Aquí marcas la explotación activa en la base de datos
        modelo.establecer_explotacion_activa(id_explotacion)

        # Llamas al método de la ventana principal para recargar encabezado y parcelas
        self.parent.actualizar_encabezado()
        self.parent.abrir_gestion_parcelas()

        # Cierra esta ventana
        self.destroy()

    
