import sqlite3


def crear_analisis(idTipoAnalisis, fecha, descripcion, resultados, id_parcela=None, id_arbol=None, db_path="olivar.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insertar análisis
    cursor.execute("""
        INSERT INTO analisis (fecha, descripcion, idTipoAnalisis, idParcela, idArbol)
        VALUES (?, ?, ?, ?, ?)
    """, (fecha, descripcion, idTipoAnalisis, id_parcela, id_arbol))

    id_analisis = cursor.lastrowid

    # Insertar resultados asociados
    for r in resultados:
        cursor.execute("""
            INSERT INTO resultado_analisis (
                idAnalisis, parametro, metodo, unidad, valor, incertidumbre, limite_cuantificacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            id_analisis,
            r['parametro'],
            r.get('metodo'),
            r.get('unidad'),
            r.get('valor'),
            r.get('incertidumbre'),
            r.get('limite_cuantificacion')
        ))

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
    cursor.execute("SELECT id, nombre FROM tipo_analisis ORDER BY nombre")
    tipos = cursor.fetchall()
    conn.close()
    return tipos

def insertar_resultado_analisis(id_analisis, parametro, metodo, unidad, valor, incertidumbre=None, limite_cuantificacion=None, db_path="olivar.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resultado_analisis (
            idAnalisis, parametro, metodo, unidad, valor, incertidumbre, limite_cuantificacion
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_analisis, parametro, metodo, unidad, valor, incertidumbre, limite_cuantificacion))

    conn.commit()
    conn.close()

def obtener_analisis_por_parcela(id_parcela, db_path="olivar.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.id, a.fecha, a.descripcion, t.nombre
        FROM analisis a
        JOIN tipo_analisis t ON a.idTipoAnalisis = t.id
        WHERE a.idParcela = ?
        ORDER BY a.fecha DESC
    """, (id_parcela,))

    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_analisis_por_arbol(id_arbol, db_path="olivar.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.id, a.fecha, a.descripcion, t.nombre
        FROM analisis a
        JOIN tipo_analisis t ON a.idTipoAnalisis = t.id
        WHERE a.idArbol = ?
        ORDER BY a.fecha DESC
    """, (id_arbol,))

    resultados = cursor.fetchall()
    conn.close()
    return resultados


def actualizar_datos_analisis(id_analisis, tipo_id, fecha, descripcion, db_path="olivar.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE analisis
        SET idTipoAnalisis = ?, fecha = ?, descripcion = ?
        WHERE id = ?
    """, (tipo_id, fecha, descripcion, id_analisis))
    conn.commit()
    conn.close()

def eliminar_resultados_analisis(id_analisis, db_path="olivar.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resultado_analisis WHERE idAnalisis = ?", (id_analisis,))
    conn.commit()
    conn.close()

def obtener_resultado_analisis_por_id(id_analisis, db_path="olivar.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Obtener metadatos del análisis
    cursor.execute("""
        SELECT fecha, descripcion
        FROM analisis
        WHERE id = ?
    """, (id_analisis,))
    meta = cursor.fetchone()

    if not meta:
        return None

    fecha, descripcion = meta

    # Obtener resultados químicos
    cursor.execute("""
        SELECT parametro, valor
        FROM resultado_analisis
        WHERE idAnalisis = ?
    """, (id_analisis,))
    resultados_raw = cursor.fetchall()

    resultados = {param: valor for param, valor in resultados_raw}

    conn.close()

    return {
        "fecha": fecha,
        "descripcion": descripcion,
        "resultados": resultados
    }

