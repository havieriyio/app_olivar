import sqlite3
import hashlib

def verificar_credenciales(usuario, contrasena):
    conn = sqlite3.connect("olivar.db")
    cursor = conn.cursor()
    
    hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

    cursor.execute("""
        SELECT id, nombre, rol FROM usuario 
        WHERE usuario = ? AND contrasena = ? AND activo = 1
    """, (usuario, hash_contrasena))

    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return {"id": resultado[0], "nombre": resultado[1], "rol": resultado[2]}
    else:
        return None
