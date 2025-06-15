import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from modelo import eliminar_por_id

class SensorViewer:
    def __init__(self, parent):
        self.ventana = Toplevel(parent)
        self.ventana.title("Gestión de Sensores")
        self.ventana.geometry("600x300")

        # Entrada para ID
        tk.Label(self.ventana, text="ID Sensor a eliminar:").pack(pady=5)
        self.sensor_id_entry = tk.Entry(self.ventana)
        self.sensor_id_entry.pack(pady=5)

        tk.Button(self.ventana, text="Eliminar sensor", command=self.eliminar_sensor).pack(pady=10)
        self.msg = tk.Label(self.ventana, text="", fg="green")
        self.msg.pack()

    def eliminar_sensor(self):
        id_str = self.sensor_id_entry.get()
        if not id_str.isdigit():
            self.msg.config(text="ID no válido", fg="red")
            return

        id_sensor = int(id_str)
        confirm = messagebox.askyesno(
            title="Confirmar eliminación",
            message=f"¿Está seguro de que desea eliminar el sensor con ID {id_sensor}?"
        )
        if not confirm:
            return

        success = eliminar_por_id("sensor", id_sensor)
        if success:
            self.msg.config(text=f"Sensor con ID {id_sensor} eliminado", fg="green")
        else:
            self.msg.config(text=f"No se encontró el sensor con ID {id_sensor}", fg="red")
