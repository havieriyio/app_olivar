import tkinter as tk
from tkinter import ttk, messagebox
from logica.analisis import crear_analisis_con_resultados, actualizar_analisis, eliminar_analisis
from logica.consulta import consultar_analisis_por_objetivo
from modelo.acceso_analisis import obtener_tipos_analisis, obtener_resultado_analisis_por_id
from modelo.acceso_parcelas import obtener_parcelas_por_explotacion
from modelo.acceso_arbol import obtener_arboles_por_parcela
from modelo.acceso_explotacion import obtener_explotacion_activa
import datetime
from tkcalendar import DateEntry

class AnalisisViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.parcelas = []
        self.arboles = []

        self.tipo_map = {}
        self.tipo_cb = None
        self.parcela_cb = None
        self.arbol_cb = None
        self.tree_analisis = None

        self.id_analisis_seleccionado = None

        self.crear_widgets()
        self.actualizar_vista()

    def crear_widgets(self):
        frame_filtros = tk.Frame(self)
        frame_filtros.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_filtros, text="Tipo de análisis:").grid(row=0, column=0)
        self.tipo_cb = ttk.Combobox(frame_filtros, state="readonly")
        self.tipo_cb.grid(row=0, column=1)

        tk.Label(frame_filtros, text="Parcela:").grid(row=1, column=0)
        self.parcela_cb = ttk.Combobox(frame_filtros, state="readonly")
        self.parcela_cb.grid(row=1, column=1)
        self.parcela_cb.bind("<<ComboboxSelected>>", lambda e: self.actualizar_arboles())

        tk.Label(frame_filtros, text="Árbol:").grid(row=2, column=0)
        self.arbol_cb = ttk.Combobox(frame_filtros, state="readonly")
        self.arbol_cb.grid(row=2, column=1)

        tk.Button(frame_filtros, text="Consultar análisis", command=self.actualizar_listado_analisis).grid(row=3, column=0, columnspan=2, pady=10)

        self.tree_analisis = ttk.Treeview(self, columns=("ID", "Fecha", "Descripción", "Tipo"), show="headings")
        self.tree_analisis.heading("ID", text="ID")
        self.tree_analisis.heading("Fecha", text="Fecha")
        self.tree_analisis.heading("Descripción", text="Descripción")
        self.tree_analisis.heading("Tipo", text="Tipo de análisis")
        self.tree_analisis.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_analisis.bind("<<TreeviewSelect>>", self.cargar_analisis_seleccionado)

        self.crear_formulario_nuevo_analisis()

    def crear_formulario_nuevo_analisis(self):
        frame_form = tk.LabelFrame(self, text="Nuevo análisis")
        frame_form.pack(fill="x", padx=10, pady=10)

        # Subframe para disposición en horizontal
        frame_contenedor = tk.Frame(frame_form)
        frame_contenedor.pack(fill="x")

        # Izquierda: Fecha y descripción
        frame_izquierdo = tk.Frame(frame_contenedor)
        frame_izquierdo.pack(side="left", padx=(0, 10), fill="y")

        tk.Label(frame_izquierdo, text="Fecha:").pack(anchor="w")
        self.fecha_entry = DateEntry(frame_izquierdo, date_pattern='dd-mm-yyyy')
        self.fecha_entry.pack(anchor="w", pady=(0, 10))

        tk.Label(frame_izquierdo, text="Descripción:").pack(anchor="w")
        self.descripcion_entry = tk.Entry(frame_izquierdo)
        self.descripcion_entry.pack(anchor="w")

        # Derecha: Tabla de resultados
        frame_derecho = tk.Frame(frame_contenedor)
        frame_derecho.pack(side="left", fill="x", expand=True)

        self.tree_resultados = ttk.Treeview(frame_derecho, columns=("Parámetro", "Valor"), show="headings", height=5)
        self.tree_resultados.heading("Parámetro", text="Parámetro")
        self.tree_resultados.heading("Valor", text="Valor")
        self.tree_resultados.pack(fill="x", expand=True)

        self.tree_resultados.bind("<Double-1>", self.editar_celda_resultado)

        for parametro in ["N", "P", "K", "Ca", "Mg"]:
            self.tree_resultados.insert("", "end", values=(parametro, ""))

        # Botones
        tk.Button(frame_form, text="Guardar análisis", command=self.guardar_analisis).pack(side="left", padx=10, pady=10)
        tk.Button(frame_form, text="Eliminar análisis", command=self.eliminar_analisis).pack(side="left", pady=10)


    def editar_celda_resultado(self, event):
        item = self.tree_resultados.identify_row(event.y)
        col = self.tree_resultados.identify_column(event.x)

        if not item or col != "#2":
            return

        x, y, width, height = self.tree_resultados.bbox(item, column=col)
        valor_actual = self.tree_resultados.set(item, column="Valor")

        entry = tk.Entry(self.tree_resultados)
        entry.insert(0, valor_actual)
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus()

        def guardar_valor(_=None):
            nuevo_valor = entry.get()
            self.tree_resultados.set(item, column="Valor", value=nuevo_valor)
            entry.destroy()

        entry.bind("<Return>", guardar_valor)
        entry.bind("<FocusOut>", guardar_valor)


    def editar_resultado(self, event):
        item_id = self.tree_resultados.identify_row(event.y)
        col = self.tree_resultados.identify_column(event.x)
        if not item_id or col != "#2":  # Solo permite editar columna "Valor"
            return

        x, y, width, height = self.tree_resultados.bbox(item_id, col)
        entry_popup = tk.Entry(self.tree_resultados)
        entry_popup.place(x=x, y=y, width=width, height=height)

        def guardar_valor(evento):
            nuevo_valor = entry_popup.get()
            self.tree_resultados.set(item_id, column="Valor", value=nuevo_valor)
            entry_popup.destroy()

        entry_popup.bind("<Return>", guardar_valor)
        entry_popup.focus()


    def guardar_analisis(self):
        tipo = self.tipo_cb.get()
        fecha = self.fecha_entry.get_date().strftime('%Y-%m-%d')
        descripcion = self.descripcion_entry.get()
        id_tipo = self.tipo_map.get(tipo)

        id_parcela = self.obtener_id_parcela_seleccionada()
        id_arbol = self.obtener_id_arbol_seleccionado()
        resultados = []

        for item in self.tree_resultados.get_children():
            parametro, valor = self.tree_resultados.item(item)["values"]
            if valor:
                try:
                    valor_num = float(valor)
                except ValueError:
                    messagebox.showerror("Error", f"El valor de {parametro} debe ser numérico.")
                    return
                resultados.append({
                    "parametro": parametro,
                    "valor": valor_num,
                    "unidad": "mg/kg",
                    "metodo": None,
                    "incertidumbre": None,
                    "limite_cuantificacion": None
                })

        if not (tipo and fecha and (id_parcela or id_arbol)):
            messagebox.showerror("Error", "Debe rellenar tipo, fecha y al menos una referencia (parcela o árbol)")
            return

        if self.id_analisis_seleccionado:
            actualizar_analisis(
                id_analisis=self.id_analisis_seleccionado,
                tipo_id=id_tipo,
                fecha=fecha,
                descripcion=descripcion,
                resultados=resultados
            )
            messagebox.showinfo("Éxito", "Análisis actualizado correctamente.")
        else:
            crear_analisis_con_resultados(
                tipo_id=id_tipo,
                fecha=fecha,
                descripcion=descripcion,
                resultados=resultados,
                id_parcela=id_parcela,
                id_arbol=id_arbol
            )
            messagebox.showinfo("Éxito", "Análisis creado correctamente.")

        self.limpiar_formulario()
        self.actualizar_listado_analisis()

    def eliminar_analisis(self):
        if not self.id_analisis_seleccionado:
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este análisis?")
        if confirmar:
            eliminar_analisis(self.id_analisis_seleccionado)
            messagebox.showinfo("Éxito", "Análisis eliminado correctamente.")
            self.limpiar_formulario()
            self.actualizar_listado_analisis()

    def limpiar_formulario(self):
        self.id_analisis_seleccionado = None
        self.fecha_entry.set_date(datetime.date.today())
        self.descripcion_entry.delete(0, tk.END)
        for item in self.tree_resultados.get_children():
            self.tree_resultados.set(item, column="Valor", value="")

    def cargar_analisis_seleccionado(self, event):
        seleccion = self.tree_analisis.selection()
        if not seleccion:
            return

        item = self.tree_analisis.item(seleccion[0])
        valores = item["values"]
        self.id_analisis_seleccionado = valores[0]

        resultado = obtener_resultado_analisis_por_id(self.id_analisis_seleccionado)
        if resultado:
            self.fecha_entry.set_date(datetime.datetime.strptime(resultado["fecha"], "%Y-%m-%d"))
            self.descripcion_entry.delete(0, tk.END)
            self.descripcion_entry.insert(0, resultado["descripcion"])

            for item in self.tree_resultados.get_children():
                parametro = self.tree_resultados.item(item)["values"][0]
                valor = resultado["resultados"].get(parametro, "")
                self.tree_resultados.set(item, column="Valor", value=valor)

    def actualizar_vista(self):
        tipos = obtener_tipos_analisis()
        self.tipo_map = {nombre: id for id, nombre in tipos}
        self.tipo_cb["values"] = list(self.tipo_map.keys())

        explotacion = obtener_explotacion_activa()
        if explotacion:
            self.parcelas = obtener_parcelas_por_explotacion(explotacion[0])
            self.parcela_cb["values"] = [f"{p[0]} - {p[1]}" for p in self.parcelas]

    def actualizar_arboles(self):
        id_parcela = self.obtener_id_parcela_seleccionada()
        if id_parcela:
            self.arboles = obtener_arboles_por_parcela(id_parcela)
            self.arbol_cb["values"] = [f"{a[0]} - {a[1]}" for a in self.arboles]

    def actualizar_listado_analisis(self):
        id_parcela = self.obtener_id_parcela_seleccionada()
        id_arbol = self.obtener_id_arbol_seleccionado()

        datos = consultar_analisis_por_objetivo(id_parcela=id_parcela, id_arbol=id_arbol)

        for item in self.tree_analisis.get_children():
            self.tree_analisis.delete(item)

        for id_analisis, fecha, descripcion, tipo in datos:
            self.tree_analisis.insert("", "end", values=(id_analisis, fecha, descripcion, tipo))

    def obtener_id_parcela_seleccionada(self):
        sel = self.parcela_cb.get()
        return int(sel.split(" - ")[0]) if sel else None

    def obtener_id_arbol_seleccionado(self):
        sel = self.arbol_cb.get()
        return int(sel.split(" - ")[0]) if sel else None
