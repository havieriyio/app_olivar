import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from modelo.acceso_analisis import crear_analisis, eliminar_analisis, obtener_todos_analisis

class AnalisisViewer:
    def __init__(self, parent):
        self.ventana = Toplevel(parent)
        self.ventana.title("Gestión de Análisis")
        self.ventana.geometry("900x500")

        self.frame = tk.Frame(self.ventana)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Formulario para crear
        tk.Label(self.frame, text="Tipo:").grid(row=0, column=0, sticky="w")
        tk.Label(self.frame, text="Tipo:").grid(row=0, column=0, sticky="w")

        # Obtener tipos desde la base de datos
        from modelo.acceso_analisis import obtener_tipos_analisis

        tipos = obtener_tipos_analisis()
        
        # Crear combobox de selección
        self.tipo_combo = ttk.Combobox(self.frame, values=tipos, state="readonly")
        self.tipo_combo.grid(row=0, column=1)
        if tipos:
            self.tipo_combo.current(0)  # seleccionar el primero por defecto

        tk.Label(self.frame, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, sticky="w")
        self.fecha_entry = tk.Entry(self.frame)
        self.fecha_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Resultado:").grid(row=2, column=0, sticky="w")
        self.resultado_entry = tk.Entry(self.frame, width=40)
        self.resultado_entry.grid(row=2, column=1, columnspan=2)

        tk.Label(self.frame, text="ID Parcela:").grid(row=3, column=0, sticky="w")
        self.parcela_entry = tk.Entry(self.frame)
        self.parcela_entry.grid(row=3, column=1)

        tk.Button(self.frame, text="Crear análisis", command=self.crear_analisis).grid(row=4, column=0, columnspan=2, pady=5)

        # Eliminar
        tk.Label(self.frame, text="ID a eliminar:").grid(row=5, column=0, sticky="w")
        self.eliminar_entry = tk.Entry(self.frame)
        self.eliminar_entry.grid(row=5, column=1)
        tk.Button(self.frame, text="Eliminar análisis", command=self.eliminar_analisis).grid(row=6, column=0, columnspan=2, pady=5)

        # Mensaje
        self.msg = tk.Label(self.frame, text="", fg="green")
        self.msg.grid(row=7, column=0, columnspan=3, sticky="w")

        # Tabla de análisis
        self.tree = ttk.Treeview(self.frame, columns=["ID", "Tipo", "Fecha", "Resultado", "Parcela"], show="headings", height=10)
        for col in ["ID", "Tipo", "Fecha", "Resultado", "Parcela"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.grid(row=8, column=0, columnspan=3, sticky="nsew")

        tk.Button(self.frame, text="Actualizar tabla", command=self.actualizar_tabla).grid(row=9, column=0, columnspan=3, pady=5)

        self.actualizar_tabla()

    def crear_analisis(self):
        tipo = self.tipo_entry.get().strip()
        fecha = self.fecha_entry.get().strip()
        resultado = self.resultado_entry.get().strip()
        parcela = self.parcela_entry.get().strip()

        if not (tipo and fecha and resultado and parcela.isdigit()):
            self.msg.config(text="⚠️ Datos incompletos o incorrectos", fg="red")
            return

        crear_analisis(tipo, fecha, resultado, int(parcela))
        self.msg.config(text="✅ Análisis creado", fg="green")
        self.actualizar_tabla()

    def eliminar_analisis(self):
        id_str = self.eliminar_entry.get().strip()
        if not id_str.isdigit():
            self.msg.config(text="⚠️ ID no válido", fg="red")
            return

        confirm = messagebox.askyesno(title="Confirmar eliminación", message=f"¿Eliminar análisis con ID {id_str}?")
        if confirm:
            eliminado = eliminar_analisis(int(id_str))
            if eliminado:
                self.msg.config(text=f"✅ Análisis con ID {id_str} eliminado", fg="green")
            else:
                self.msg.config(text=f"⚠️ Análisis no encontrado", fg="red")
            self.actualizar_tabla()

    def actualizar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for a in obtener_todos_analisis():
            self.tree.insert("", "end", values=a)