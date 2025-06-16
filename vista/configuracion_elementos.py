import tkinter as tk
from tkinter import ttk, messagebox
from modelo.acceso_elementos import obtener_elementos, insertar_elemento, actualizar_elemento, eliminar_elemento


class ConfiguracionElementosViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.crear_widgets()
        self.cargar_elementos()

    def crear_widgets(self):
        tk.Label(self, text="Configuración de elementos y valores sugeridos", font=("Arial", 14, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Sugerido"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre del parámetro")
        self.tree.heading("Sugerido", text="Valor sugerido")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=200)
        self.tree.column("Sugerido", width=120, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree.bind("<Double-1>", self.editar_celda)

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Añadir nuevo", command=self.abrir_formulario_nuevo).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Eliminar seleccionado", command=self.eliminar_elemento).pack(side="left", padx=5)

    def cargar_elementos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        elementos = obtener_elementos()
        for elem in elementos:
            self.tree.insert("", "end", values=elem)

    def editar_celda(self, event):
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if not item or col == "#1":
            return  # No editar la columna ID

        col_nombre = {"#2": "Nombre", "#3": "Sugerido"}[col]
        x, y, width, height = self.tree.bbox(item, column=col)
        valor_actual = self.tree.set(item, column=col_nombre)

        entry = tk.Entry(self.tree)
        entry.insert(0, valor_actual)
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus()

        def guardar(_=None):
            nuevo_valor = entry.get()
            self.tree.set(item, column=col_nombre, value=nuevo_valor)
            entry.destroy()
            self.guardar_edicion(item)

        entry.bind("<Return>", guardar)
        entry.bind("<FocusOut>", guardar)

    def guardar_edicion(self, item_id):
        valores = self.tree.item(item_id)["values"]
        try:
            actualizar_elemento(valores[0], valores[1], float(valores[2]))
            messagebox.showinfo("Guardado", "Elemento actualizado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "El valor sugerido debe ser numérico.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def abrir_formulario_nuevo(self):
        ventana = tk.Toplevel(self)
        ventana.title("Nuevo elemento")

        tk.Label(ventana, text="Nombre del parámetro:").grid(row=0, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(ventana)
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(ventana, text="Valor sugerido:").grid(row=1, column=0, padx=10, pady=5)
        sugerido_entry = tk.Entry(ventana)
        sugerido_entry.grid(row=1, column=1, padx=10, pady=5)

        def guardar():
            nombre = nombre_entry.get().strip()
            sugerido = sugerido_entry.get().strip()
            if not nombre or not sugerido:
                messagebox.showwarning("Faltan datos", "Debe completar todos los campos.")
                return
            try:
                insertar_elemento(nombre, float(sugerido))
                ventana.destroy()
                self.cargar_elementos()
                messagebox.showinfo("Éxito", "Elemento añadido.")
            except ValueError:
                messagebox.showerror("Error", "El valor sugerido debe ser numérico.")

        tk.Button(ventana, text="Guardar", command=guardar).grid(row=2, column=0, columnspan=2, pady=10)

    def eliminar_elemento(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Seleccione uno", "Debe seleccionar un elemento para eliminar.")
            return
        item = self.tree.item(seleccion[0])
        id_elemento = item["values"][0]
        confirmar = messagebox.askyesno("Confirmar", "¿Desea eliminar este elemento?")
        if confirmar:
            eliminar_elemento(id_elemento)
            self.cargar_elementos()
            messagebox.showinfo("Eliminado", "Elemento eliminado correctamente.")
