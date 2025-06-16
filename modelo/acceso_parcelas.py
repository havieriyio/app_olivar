import sqlite3
from modelo.db import conectar 

DB_PATH = "olivar.db"

def obtener_todas_parcelas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, superficie, ubicacion FROM parcela ORDER BY id")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def insertar_parcela(nombre, superficie, ubicacion, idExplotacion):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO parcela (nombre, superficie, ubicacion, idExplotacion)
        VALUES (?, ?, ?,?)
    """, (nombre, superficie, ubicacion,idExplotacion))
    conn.commit()
    conn.close()

def actualizar_parcela(id_parcela, nombre, superficie, ubicacion):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE parcela SET nombre = ?, superficie = ?, ubicacion = ?
        WHERE id = ?
    """, (nombre, superficie, ubicacion, id_parcela))
    conn.commit()
    conn.close()

def borrar_parcela(id_parcela):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM parcela WHERE id = ?", (id_parcela,))
    conn.commit()
    conn.close()

def obtener_parcelas_por_explotacion(id_explotacion):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, superficie, ubicacion
        FROM parcela
        WHERE idExplotacion = ?
    """, (id_explotacion,))

    resultados = cursor.fetchall()
    conn.close()
    return resultados
