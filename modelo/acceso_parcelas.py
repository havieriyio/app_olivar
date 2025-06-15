import sqlite3

DB_PATH = "olivar.db"

def obtener_todas_parcelas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, superficie, ubicacion FROM parcela ORDER BY id")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def insertar_parcela(nombre, superficie, ubicacion):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO parcela (nombre, superficie, ubicacion)
        VALUES (?, ?, ?)
    """, (nombre, superficie, ubicacion))
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
