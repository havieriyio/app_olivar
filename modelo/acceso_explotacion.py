import sqlite3

DB_PATH = "olivar.db"

def obtener_conexion():
    return sqlite3.connect(DB_PATH)

def obtener_todas_explotaciones():
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, ubicacion, activa FROM explotacion ORDER BY id")
        return cursor.fetchall()

def insertar_explotacion(nombre, ubicacion):
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO explotacion (nombre, ubicacion) VALUES (?, ?)", (nombre, ubicacion))
        conn.commit()

def eliminar_explotacion(id_explotacion):
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM explotacion WHERE id = ?", (id_explotacion,))
        conn.commit()

def establecer_explotacion_activa(id_explotacion):
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE explotacion SET activa = 0")
        cursor.execute("UPDATE explotacion SET activa = 1 WHERE id = ?", (id_explotacion,))
        conn.commit()

def obtener_explotacion_activa():
    with obtener_conexion() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM explotacion WHERE activa = 1")
        return cursor.fetchone()

