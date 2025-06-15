from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk, messagebox
from modelo.acceso_parcelas import (
    obtener_todas_parcelas,
    insertar_parcela,
    actualizar_parcela,
    borrar_parcela
)

from modelo.acceso_arbol import obtener_arboles_por_parcela,obtener_variedades, insertar_arbol

import datetime

class ParcelaViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.gestion_frame = tk.Frame(parent)
        self.gestion_frame.pack(fill="both", expand=True)

        # Contenedor dividido en dos paneles
        self.panel_contenido = tk.Frame(self.gestion_frame)
        self.panel_contenido.pack(fill="both", expand=True)

        # Panel izquierdo: parcelas
        self.frame_izquierda = tk.Frame(self.panel_contenido)
        self.frame_izquierda.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Panel derecho: árboles
        self.frame_derecha = tk.Frame(self.panel_contenido, bg="white")
        self.frame_derecha.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Árbol de parcelas
        self.tree_parcelas = ttk.Treeview(
            self.frame_izquierda,
            columns=["ID", "Nombre", "Superficie", "Ubicacion"],
            show="headings",
            height=12
        )
        for col in ["ID", "Nombre", "Superficie", "Ubicacion"]:
            self.tree_parcelas.heading(col, text=col)
        self.tree_parcelas.pack(fill="both", expand=True)

        # Evento de selección
        self.tree_parcelas.bind("<<TreeviewSelect>>", self.on_parcela_seleccionada)

        # Árbol de árboles
        self.tree_arboles = ttk.Treeview(
            self.frame_derecha,
            columns=["ID", "Variedad", "Fecha plantación"],
            show="headings",
            height=12
        )
        for col in ["ID", "Variedad", "Fecha plantación"]:
            self.tree_arboles.heading(col, text=col)
        self.tree_arboles.pack(fill="both", expand=True)
        boton_frame_arbol = tk.Frame(self.frame_derecha)

        # Botón para añadir árbol.
        boton_frame_arbol.pack(pady=5)

        tk.Button(boton_frame_arbol, text="Añadir árbol", command=self.abrir_formulario_nuevo_arbol).pack(side="left", padx=5)


        # Botones de gestión
        btn_frame = tk.Frame(self.frame_izquierda)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Añadir", command=self.abrir_formulario_nueva).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Modificar", command=self.abrir_formulario_modificar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Borrar", command=self.borrar_parcela).pack(side="left", padx=5)


        self.cargar_parcelas()

    def cargar_parcelas(self):
        for i in self.tree_parcelas.get_children():
            self.tree_parcelas.delete(i)

        for id_, nombre, superficie, ubicacion in obtener_todas_parcelas():
            self.tree_parcelas.insert("", "end", values=(id_, nombre, superficie, ubicacion))

    def abrir_formulario_nueva(self):
        self._abrir_formulario("nueva")

    def abrir_formulario_modificar(self):
        seleccion = self.tree_parcelas.selection()
        if not seleccion:
            messagebox.showwarning("Modificar", "Seleccione una parcela")
            return
        datos = self.tree_parcelas.item(seleccion[0])["values"]
        self._abrir_formulario("modificar", datos)

    def _abrir_formulario(self, modo, datos=None):
        win = tk.Toplevel(self.gestion_frame)
        win.update_idletasks()
        ancho, alto = 300, 240
        x = win.winfo_screenwidth() // 2 - ancho // 2
        y = win.winfo_screenheight() // 2 - alto // 2
        win.geometry(f"{ancho}x{alto}+{x}+{y}")
        win.title("Parcela")

        campos = {
            "nombre": tk.StringVar(),
            "superficie": tk.StringVar(),
            "ubicacion": tk.StringVar()
        }

        etiquetas = {
            "nombre": "Nombre:",
            "superficie": "Superficie (ha):",
            "ubicacion": "Ubicación:"
        }

        for campo, etiqueta in etiquetas.items():
            tk.Label(win, text=etiqueta).pack()
            tk.Entry(win, textvariable=campos[campo]).pack()

        if datos:
            campos["nombre"].set(datos[1])
            campos["superficie"].set(datos[2])
            campos["ubicacion"].set(datos[3])

        def guardar():
            nombre = campos["nombre"].get().strip()
            superficie = campos["superficie"].get().strip()
            ubicacion = campos["ubicacion"].get().strip()

            if not nombre:
                messagebox.showwarning("Error", "El nombre es obligatorio.")
                return

            if modo == "nueva":
                insertar_parcela(nombre, superficie, ubicacion)
            else:
                actualizar_parcela(datos[0], nombre, superficie, ubicacion)

            win.destroy()
            self.cargar_parcelas()

        tk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def borrar_parcela(self):
        seleccion = self.tree_parcelas.selection()
        if not seleccion:
            messagebox.showwarning("Borrar", "Seleccione una parcela")
            return
        datos = self.tree_parcelas.item(seleccion[0])["values"]
        respuesta = messagebox.askyesno("Confirmar", f"¿Borrar parcela '{datos[1]}'?")
        if respuesta:
            borrar_parcela(datos[0])
            self.cargar_parcelas()


    def on_parcela_seleccionada(self, event):
        seleccion = self.tree_parcelas.selection()
        if not seleccion:
            return

        item = self.tree_parcelas.item(seleccion[0])
        id_parcela = item["values"][0]

        arboles = obtener_arboles_por_parcela(id_parcela)

        self.tree_arboles.delete(*self.tree_arboles.get_children())
        for arbol in arboles:
            self.tree_arboles.insert("", "end", values=arbol)

    def abrir_formulario_nuevo_arbol(self):
        # Obtener la parcela seleccionada
        seleccion = self.tree_parcelas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una parcela antes de añadir un árbol.")
            return

        item = self.tree_parcelas.item(seleccion[0])
        id_parcela = item["values"][0]

        # Crear ventana emergente
        win = tk.Toplevel(self.gestion_frame)
        win.title("Nuevo árbol")
        win.geometry("300x200")

        # Obtener variedades
        variedades = obtener_variedades()
        if not variedades:
            messagebox.showerror("Error", "No hay variedades disponibles.")
            win.destroy()
            return

        tk.Label(win, text="Variedad:").pack()
        variedad_var = tk.StringVar()
        combo_variedad = ttk.Combobox(win, textvariable=variedad_var, state="readonly")
        combo_variedad["values"] = [f"{v[0]} - {v[1]}" for v in variedades]
        combo_variedad.pack()

        # Botón calendario.
        tk.Label(win, text="Fecha plantación:").pack()
        fecha_cal = DateEntry(win, date_pattern='dd-mm-yyyy')
        fecha_cal.pack()

        def guardar():
            if not variedad_var.get() or fecha_cal.get_date() is None:
                messagebox.showwarning("Error", "Todos los campos son obligatorios.")
                return

            try:
                fecha_obj = fecha_cal.get_date()  # retorna datetime.date
                fecha_str = fecha_obj.strftime("%Y-%m-%d")  # lo convertimos a ISO para guardar en SQLite
            except ValueError:
                messagebox.showerror("Error", "La fecha debe tener formato DD-MM-YYYY.")
                return
            try:
                id_variedad = int(variedad_var.get().split(" - ")[0])
                fecha_obj = fecha_cal.get_date()
                fecha_str = fecha_obj.strftime("%Y-%m-%d")  # formato ISO para SQLite
                insertar_arbol(id_parcela, id_variedad, fecha_str)
                self.on_parcela_seleccionada(None)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el árbol: {e}")  


        tk.Button(win, text="Guardar", command=guardar).pack(pady=10)