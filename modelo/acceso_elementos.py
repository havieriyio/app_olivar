import sqlite3

def obtener_elementos():
    conn = sqlite3.connect("olivar.db")
    cur = conn.cursor()
    cur.execute("SELECT id, nombre, valor_sugerido FROM elementos ORDER BY nombre")
    datos = cur.fetchall()
    conn.close()
    return datos

def insertar_elemento(nombre, sugerido):
    conn = sqlite3.connect("olivar.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO elementos (nombre, valor_sugerido) VALUES (?, ?)", (nombre, sugerido))
    conn.commit()
    conn.close()

def actualizar_elemento(id_elem, nombre, sugerido):
    conn = sqlite3.connect("olivar.db")
    cur = conn.cursor()
    cur.execute("UPDATE elementos SET nombre = ?, valor_sugerido = ? WHERE id = ?", (nombre, sugerido, id_elem))
    conn.commit()
    conn.close()

def eliminar_elemento(id_elem):
    conn = sqlite3.connect("olivar.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM elementos WHERE id = ?", (id_elem,))
    conn.commit()
    conn.close()
