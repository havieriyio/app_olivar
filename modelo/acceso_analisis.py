import sqlite3

def crear_analisis(tipo, fecha, resultado, id_parcela, db_path="olivar.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Buscar ID del tipo de análisis
    cursor.execute("SELECT id FROM tipo_analisis WHERE nombre = ?", (tipo,))
    tipo_row = cursor.fetchone()
    if tipo_row is None:
        raise ValueError(f"Tipo de análisis '{tipo}' no encontrado.")
    tipo_id = tipo_row[0]

    # Insertar análisis
    cursor.execute("""
        INSERT INTO analisis (fecha, descripcion, resultados, tipo_analisis_id, parcela_id)
        VALUES (?, ?, ?, ?, ?)
    """, (fecha, f"Análisis {tipo} automático", resultado, tipo_id, id_parcela))

    conn.commit()
    conn.close()


def eliminar_analisis(id_analisis, db_path="olivar.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analisis WHERE id = ?", (id_analisis,))
    cambios = conn.total_changes
    conn.commit()
    conn.close()
    return cambios > 0

def obtener_todos_analisis(db_path="olivar.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT a.id, ta.nombre, a.fecha, a.resultado, p.nombre FROM analisis a JOIN tipo_analisis ta ON a.id_tipo_analisis = ta.id LEFT JOIN parcela p ON a.id_parcela = p.id ORDER BY a.fecha DESC")
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_tipos_analisis(db_path="olivar.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM tipo_analisis WHERE activo = 1")
    tipos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tipos