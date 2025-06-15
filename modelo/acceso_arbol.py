import sqlite3

DB_PATH = "olivar.db"

def obtener_variedades():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM variedad ORDER BY nombre")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def obtener_todos_los_arboles():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.codigo, v.nombre, a.edad, a.fecha_plantacion, p.nombre
        FROM arbol a
        LEFT JOIN variedad v ON a.variedad_id = v.id
        LEFT JOIN parcela p ON a.parcela_id = p.id
        ORDER BY a.id
    """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def obtener_arboles_por_parcela(id_parcela):
    conn = sqlite3.connect("olivar.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, v.nombre, a.fecha_plantacion
        FROM arbol a
        JOIN variedad v ON a.id_variedad = v.id
        WHERE a.id_parcela = ?
        ORDER BY a.fecha_plantacion ASC
    """, (id_parcela,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def insertar_arbol(id_parcela, id_variedad, fecha_plantacion):
    conn = sqlite3.connect("olivar.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO arbol (id_parcela, id_variedad, fecha_plantacion)
        VALUES (?, ?, ?)
    """, (id_parcela, id_variedad, fecha_plantacion))
    conn.commit()
    conn.close()
    
def actualizar_arbol(id_arbol, codigo, variedad_id, edad, fecha_plantacion, parcela_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE arbol
        SET codigo = ?, variedad_id = ?, edad = ?, fecha_plantacion = ?, parcela_id = ?
        WHERE id = ?
    """, (codigo, variedad_id, edad, fecha_plantacion, parcela_id, id_arbol))
    conn.commit()
    conn.close()

def borrar_arbol(id_arbol):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM arbol WHERE id = ?", (id_arbol,))
    conn.commit()
    conn.close()
