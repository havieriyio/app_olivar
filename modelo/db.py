# db.py
import sqlite3

DB_PATH = "olivar.db"

def validar_login(usuario, contraseña, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM usuario WHERE nombre=? AND contraseña=?", (usuario, contraseña))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def registrar_sensor(tipo, descripcion, fecha_registro, db_path=DB_PATH):
    if tipo not in ["temperatura", "composición"]:
        raise ValueError("Tipo de sensor no válido")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor (tipo, descripcion, fecha_registro) VALUES (?, ?, ?)",
        (tipo, descripcion, fecha_registro)
    )
    conn.commit()
    conn.close()
    return True

def insertar_analisis(tipo, fecha, resultado, id_parcela, db_path=DB_PATH):
    if tipo not in ["foliar", "suelo"]:
        raise ValueError("Tipo de análisis no válido")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analisis (tipo, fecha, resultado, id_parcela) VALUES (?, ?, ?, ?)",
        (tipo, fecha, resultado, id_parcela)
    )
    conn.commit()
    conn.close()
    return True

def insertar_tratamiento(descripcion, fecha, confirmado, id_parcela, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tratamiento (descripcion, fecha, confirmado, id_parcela) VALUES (?, ?, ?, ?)",
        (descripcion, fecha, confirmado, id_parcela)
    )
    conn.commit()
    conn.close()
    return True

def vincular_sensor_parcela(id_sensor, id_parcela, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sensor_parcela (id_sensor, id_parcela) VALUES (?, ?)",
        (id_sensor, id_parcela)
    )
    conn.commit()
    conn.close()
    return True

def obtener_datos_parcela(id_parcela, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Sensores vinculados
    cursor.execute("""
        SELECT s.id, s.tipo, s.descripcion, s.fecha_registro
        FROM sensor s
        JOIN sensor_parcela sp ON s.id = sp.id_sensor
        WHERE sp.id_parcela = ?
    """, (id_parcela,))
    sensores = cursor.fetchall()

    # 2. Análisis de suelo y foliar
    cursor.execute("""
        SELECT tipo, fecha, resultado
        FROM analisis
        WHERE id_parcela = ?
        ORDER BY fecha DESC
    """, (id_parcela,))
    analisis = cursor.fetchall()

    # 3. Tratamientos aplicados
    cursor.execute("""
        SELECT descripcion, fecha, confirmado
        FROM tratamiento
        WHERE id_parcela = ?
        ORDER BY fecha DESC
    """, (id_parcela,))
    tratamientos = cursor.fetchall()

    conn.close()

    return {
        "sensores": sensores,
        "analisis": analisis,
        "tratamientos": tratamientos
    }

def obtener_todas_parcelas(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM parcela ORDER BY id")
    parcelas = cursor.fetchall()
    conn.close()
    return parcelas

def crear_parcela(nombre, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO parcela (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()

def eliminar_parcela(id_parcela, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM parcela WHERE id = ?", (id_parcela,))
    cambios = conn.total_changes
    conn.commit()
    conn.close()
    return cambios > 0


def eliminar_por_id(tabla, id_valor, db_path="olivar_ejemplo.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {tabla} WHERE id = ?", (id_valor,))
    cambios = conn.total_changes
    conn.commit()
    conn.close()
    return cambios > 0