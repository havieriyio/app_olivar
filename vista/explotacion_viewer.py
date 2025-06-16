import tkinter as tk
from tkinter import messagebox,ttk
from modelo import acceso_explotacion as modelo
from modelo.acceso_explotacion import obtener_explotacion_activa,obtener_todas_explotaciones
from modelo.acceso_parcelas import obtener_parcelas_por_explotacion

class ExplotacionViewer(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.title("Gestión de Explotaciones")
        self.geometry("600x400")

        self.id_explotacion_activa = None
        activa = obtener_explotacion_activa()
        if activa:
            self.id_explotacion_activa = activa[0]

        # Treeview para mostrar explotaciones
        self.tree = ttk.Treeview(self, columns=("Nombre", "Ubicación"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Ubicación", text="Ubicación")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame de botones
        self.frame_botones = tk.Frame(self)
        self.frame_botones.pack(pady=10)
        '''
        self.frame_botones = tk.Frame(self.win)
        self.frame_botones.pack(pady=10)'''

        # Botón activar
        tk.Button(self.frame_botones, text="Activar", command=self.activar_explotacion_seleccionada).grid(row=0, column=0, padx=5)

        tk.Button(self.frame_botones, text="Añadir", command=self.anadir).grid(row=0, column=0, padx=5)
        tk.Button(self.frame_botones, text="Eliminar", command=self.eliminar).grid(row=0, column=1, padx=5)
        tk.Button(self.frame_botones, text="Activar", command=self.activar_explotacion_seleccionada).grid(row=0, column=2, padx=5)
        
        # Cargar explotaciones en la tabla
        self.cargar_explotaciones()
        
        self.recargar()

    def recargar(self):
        # Limpia el Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        explotaciones = obtener_todas_explotaciones()  # o como se llame tu función
        for expl in explotaciones:
            self.tree.insert("", "end", iid=expl[0], values=(expl[1], expl[2]))

        # Selecciona la explotación activa si está disponible
        if self.id_explotacion_activa:
            self.tree.selection_set(self.id_explotacion_activa)
            self.tree.see(self.id_explotacion_activa)


    def anadir(self):
        top = tk.Toplevel(self)
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
        seleccion = self.tree.selection()

        if not seleccion:
            return  # Nada seleccionado

        id_explotacion = int(seleccion[0])  # El Treeview usa el id como iid

        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar esta explotación?"
        )

        if confirmacion:
            modelo.eliminar_explotacion(id_explotacion)
            self.recargar()

    def activar(self, id_explotacion):
        modelo.establecer_explotacion_activa(id_explotacion)
        self.master.actualizar_encabezado()
        self.master.abrir_gestion_parcelas()
        self.destroy()


    def seleccionar_explotacion(self, id_explotacion):
        # Aquí marcas la explotación activa en la base de datos
        modelo.establecer_explotacion_activa(id_explotacion)

        # Llamas al método de la ventana principal para recargar encabezado y parcelas
        self.parent.actualizar_encabezado()
        self.parent.abrir_gestion_parcelas()

        # Cierra esta ventana
        self.destroy()

    
    def cargar_explotaciones(self):
        explotaciones = obtener_todas_explotaciones()  # Devuelve lista de tuplas (id, nombre, ubicacion)
        for exp in explotaciones:
            self.tree.insert("", "end", iid=exp[0], values=(exp[1], exp[2]))

    def activar_explotacion_seleccionada(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        id_explotacion = int(seleccion[0])
        self.activar(id_explotacion)