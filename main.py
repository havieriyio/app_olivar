from vista.login_viewer import LoginViewer
from vista.ventana_principal import VentanaPrincipal

def iniciar_aplicacion(usuario):
    app = VentanaPrincipal(usuario)
    app.mainloop()

if __name__ == "__main__":
    login = LoginViewer(iniciar_aplicacion)
    login.mainloop()
