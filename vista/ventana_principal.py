import tkinter as tk
from tkinter import ttk
from .parcela_viewer import ParcelaViewer
from .analisis_viewer import AnalisisViewer

class VentanaPrincipal(tk.Tk):
    def __init__(self, usuario):
        super().__init__()
        self.title("Sistema de Análisis de Olivar")
        self.geometry("1500x600")

        tk.Label(self, text=f"Bienvenido, {usuario['nombre']}", font=("Arial", 14)).pack(fill="x", padx=10, pady=5)

        self.menu_frame = tk.Frame(self, bg="#dddddd", width=200)
        self.menu_frame.pack(side="left", fill="y")

        tk.Button(self.menu_frame, text="Parcelas", command=self.abrir_gestion_parcelas).pack(pady=5, fill="x")
        tk.Button(self.menu_frame, text="Tipos de análisis", command=self.abrir_gestion_analisis).pack(pady=5, fill="x")
        tk.Button(self.menu_frame, text="Cerrar sesión", command=self.destroy).pack(side="bottom", pady=10)

        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(side="right", expand=True, fill="both")

    def abrir_gestion_parcelas(self):
        ParcelaViewer(self)

    def abrir_gestion_analisis(self):
        AnalisisViewer(self)
