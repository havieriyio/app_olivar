from vista.ventana_principal import VentanaPrincipal

if __name__ == "__main__":
    # Usuario ficticio para pruebas
    usuario_ficticio = {
        "id": 1,
        "nombre": "Admin de prueba",
        "rol": "admin"
    }

    app = VentanaPrincipal(usuario_ficticio)
    app.mainloop()
