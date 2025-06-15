# tests/test_consulta.py
import unittest
import sqlite3
import os
from modelo import obtener_datos_parcela

TEST_DB = "test_olivar.db"

def crear_datos_combinados():
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE parcela (id INTEGER PRIMARY KEY, nombre TEXT);
        CREATE TABLE sensor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            descripcion TEXT,
            fecha_registro TEXT NOT NULL
        );
        CREATE TABLE sensor_parcela (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_sensor INTEGER,
            id_parcela INTEGER,
            FOREIGN KEY (id_sensor) REFERENCES sensor(id),
            FOREIGN KEY (id_parcela) REFERENCES parcela(id)
        );
        CREATE TABLE analisis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            fecha TEXT NOT NULL,
            resultado TEXT,
            id_parcela INTEGER,
            FOREIGN KEY (id_parcela) REFERENCES parcela(id)
        );
        CREATE TABLE tratamiento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            fecha TEXT NOT NULL,
            confirmado INTEGER DEFAULT 0,
            id_parcela INTEGER,
            FOREIGN KEY (id_parcela) REFERENCES parcela(id)
        );

        INSERT INTO parcela (id, nombre) VALUES (1, 'Sur');
        INSERT INTO sensor (tipo, descripcion, fecha_registro) VALUES ('temperatura', 'Sensor A', '2025-06-01');
        INSERT INTO sensor_parcela (id_sensor, id_parcela) VALUES (1, 1);
        INSERT INTO analisis (tipo, fecha, resultado, id_parcela) VALUES ('foliar', '2025-06-10', 'Déficit nitrógeno', 1);
        INSERT INTO tratamiento (descripcion, fecha, confirmado, id_parcela) VALUES ('Fertilizante N', '2025-06-11', 1, 1);
    """)
    conn.commit()
    conn.close()

class TestConsultaParcela(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        crear_datos_combinados()

    def test_datos_parcela_completo(self):
        datos = obtener_datos_parcela(1, db_path=TEST_DB)
        self.assertEqual(len(datos["sensores"]), 1)
        self.assertEqual(len(datos["analisis"]), 1)
        self.assertEqual(len(datos["tratamientos"]), 1)
        self.assertIn("Déficit", datos["analisis"][0][2])

    def test_parcela_sin_datos(self):
        datos = obtener_datos_parcela(99, db_path=TEST_DB)
        self.assertEqual(datos["sensores"], [])
        self.assertEqual(datos["analisis"], [])
        self.assertEqual(datos["tratamientos"], [])

    @classmethod
    def tearDownClass(cls):
        os.remove(TEST_DB)

if __name__ == '__main__':
    unittest.main()
