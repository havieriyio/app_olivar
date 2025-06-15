import tkinter as tk
from tkinter import ttk, messagebox
from modelo.acceso_arbol import (
    obtener_todos_los_arboles,
    insertar_arbol,
    actualizar_arbol,
    borrar_arbol,
    obtener_todas_las_variedades
)
from modelo.acceso_parcelas import obtener_todas_parcelas

class ArbolViewer:
    def __init__(self, master, id_parcela):
        self.id_parcela = id_parcela
        self.ventana = tk.Toplevel(master)
        self.ventana.title(f"Árboles de la parcela {id_parcela}")

        # Aquí cargarías los árboles desde la base de datos
        self.treeview = ttk.Treeview(self.ventana, columns=("id", "variedad", "fecha_plantacion"), show='headings')
        self.treeview.heading("id", text="ID")
        self.treeview.heading("variedad", text="Variedad")
        self.treeview.heading("fecha_plantacion", text="Fecha de Plantación")
        self.treeview.pack(fill='both', expand=True)

        self.cargar_arboles()

    def cargar_arboles(self):
        from modelo.acceso_arbol import obtener_arboles_por_parcela
        arboles = obtener_arboles_por_parcela(self.id_parcela)
        for arbol in arboles:
            self.treeview.insert("", "end", values=arbol)


    def abrir_formulario_nuevo(self):
        self._abrir_formulario("nuevo")

    def abrir_formulario_modificar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Modificar", "Seleccione un árbol")
            return
        datos = self.tree.item(seleccion[0])["values"]
        self._abrir_formulario("modificar", datos)

    def _abrir_formulario(self, modo, datos=None):
        win = tk.Toplevel(self.gestion_frame)
        win.title("Formulario de Árbol")

        # Datos auxiliares para combos
        variedades = obtener_todas_las_variedades()
        parcelas = obtener_todas_parcelas()

        variedad_ids = [v[0] for v in variedades]
        variedad_nombres = [v[1] for v in variedades]

        parcela_ids = [p[0] for p in parcelas]
        parcela_nombres = [p[1] for p in parcelas]

        campos = {
            "codigo": tk.StringVar(),
            "variedad": tk.StringVar(),
            "edad": tk.StringVar(),
            "fecha": tk.StringVar(),
            "parcela": tk.StringVar()
        }

        labels = ["Código:", "Variedad:", "Edad:", "Fecha de plantación (YYYY-MM-DD):", "Parcela:"]
        for i, campo in enumerate(campos):
            tk.Label(win, text=labels[i]).pack()
            if campo in ("variedad", "parcela"):
                opciones = variedad_nombres if campo == "variedad" else parcela_nombres
                ttk.Combobox(win, textvariable=campos[campo], values=opciones, state="readonly").pack()
            else:
                tk.Entry(win, textvariable=campos[campo]).pack()

        if datos:
            campos["codigo"].set(datos[1])
            campos["variedad"].set(datos[2])
            campos["edad"].set(datos[3])
            campos["fecha"].set(datos[4])
            campos["parcela"].set(datos[5])

        def guardar():
            try:
                codigo = campos["codigo"].get().strip()
                variedad_id = variedad_ids[variedad_nombres.index(campos["variedad"].get())]
                edad = int(campos["edad"].get())
                fecha = campos["fecha"].get().strip()
                parcela_id = parcela_ids[parcela_nombres.index(campos["parcela"].get())]

                if not codigo:
                    raise ValueError("El código es obligatorio")

                if modo == "nuevo":
                    insertar_arbol(codigo, variedad_id, edad, fecha, parcela_id)
                else:
                    actualizar_arbol(datos[0], codigo, variedad_id, edad, fecha, parcela_id)

                win.destroy()
                self.cargar_arboles()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def borrar_arbol(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Borrar", "Seleccione un árbol")
            return
        datos = self.tree.item(seleccion[0])["values"]
        if messagebox.askyesno("Confirmar", f"¿Borrar el árbol '{datos[1]}'?"):
            borrar_arbol(datos[0])
            self.cargar_arboles()
