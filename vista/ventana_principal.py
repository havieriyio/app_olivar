import tkinter as tk
from tkinter import ttk
from .parcela_viewer import ParcelaViewer
from .analisis_viewer import AnalisisViewer
from .explotacion_viewer import ExplotacionViewer
from modelo.acceso_explotacion import obtener_explotacion_activa

class VentanaPrincipal(tk.Tk):
    def __init__(self,usuario):
        super().__init__()
        
        self.usuario = usuario
        self.title("Sistema de Análisis de Olivar")
        self.geometry("1500x600")

        self.panel_parcela = None
        
        explotacion = obtener_explotacion_activa()
        nombre_explotacion = explotacion[1] if explotacion else "Ninguna"
        
       # Aquí creo el frame del menú
        self.menu_frame = tk.Frame(self, bg="#dddddd", width=200)
        self.menu_frame.pack(side="left", fill="y")

        self.label_usuario_explotacion = tk.Label(self, font=("Arial", 10), anchor="w")
        self.label_usuario_explotacion.pack(fill=tk.X, padx=10, pady=5)

        # Frame dedicado para la cabecera.
        self.frame_encabezado = tk.Frame(self)
        self.frame_encabezado.pack(fill="x")

        self.label_explotacion = tk.Label(self.frame_encabezado, font=("Arial", 14))
        self.label_explotacion.pack(fill="x", padx=10, pady=5)
        
        self.actualizar_encabezado()

        tk.Button(self.menu_frame, text="Explotaciones", command=self.abrir_gestion_explotaciones).pack(fill="x", pady=5)
        tk.Button(self.menu_frame, text="Tipos de análisis", command=self.abrir_gestion_analisis).pack(pady=5, fill="x")
        tk.Button(self.menu_frame, text="Cerrar sesión", command=self.destroy).pack(side="bottom", pady=10,fill="x")

        self.contenedor_panel = tk.Frame(self)
        self.contenedor_panel.pack(fill='both', expand=True)

        self.frame_parcelas = None
        self.frame_analisis = None

        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(side="right", expand=True, fill="both")

    
    def abrir_gestion_parcelas(self):
        self.ocultar_frames()

        # Siempre crea una nueva instancia para que las parcelas reflejen la explotación activa
        self.frame_parcelas = ParcelaViewer(self.contenedor_panel)
        self.frame_parcelas.pack(fill='both', expand=True)

        
            
    def abrir_gestion_analisis(self):
        self.ocultar_frames()

        # Crear siempre una nueva instancia garantiza que los datos se actualicen
        self.frame_analisis = AnalisisViewer(self.contenedor_panel)
        self.frame_analisis.pack(fill='both', expand=True)

        
    def ocultar_frames(self):
        for widget in self.contenedor_panel.winfo_children():
            widget.pack_forget()

    def abrir_gestion_explotaciones(self):
        def on_close():
            self.actualizar_encabezado()

            # Borra las vistas para forzar su recarga tras cambio de explotación
            self.frame_parcelas = None
            self.frame_analisis = None

            self.abrir_gestion_parcelas()

        ventana = ExplotacionViewer(self)
        ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), on_close()])


    def actualizar_encabezado(self):
        usuario = getattr(self, "usuario", "Desconocido")
        explotacion = obtener_explotacion_activa()
        nombre_explotacion = explotacion[1] if explotacion else "Ninguna"

        self.label_explotacion.config(text=f"Bienvenido, {usuario['nombre']} | Explotación activa: {nombre_explotacion}")

    