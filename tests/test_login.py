# tests/test_login.py
import unittest
import sqlite3
import os
from modelo import validar_login

TEST_DB = "test_olivar.db"

def crear_base_datos_test():
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE usuario (id INTEGER PRIMARY KEY, nombre TEXT, contraseña TEXT)")
    cursor.execute("INSERT INTO usuario (nombre, contraseña) VALUES ('testuser', 'testpass')")
    conn.commit()
    conn.close()

class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        crear_base_datos_test()

    def test_login_valido(self):
        self.assertTrue(validar_login('testuser', 'testpass', db_path=TEST_DB))

    def test_login_invalido_usuario(self):
        self.assertFalse(validar_login('usuario_incorrecto', 'testpass', db_path=TEST_DB))

    def test_login_invalido_contraseña(self):
        self.assertFalse(validar_login('testuser', 'contraseña_mal', db_path=TEST_DB))

    @classmethod
    def tearDownClass(cls):
        os.remove(TEST_DB)

if __name__ == '__main__':
    unittest.main()
