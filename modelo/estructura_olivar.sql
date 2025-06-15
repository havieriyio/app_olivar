
-- roles
CREATE TABLE rol (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

-- usuarios
CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    id_rol INTEGER,
    FOREIGN KEY (id_rol) REFERENCES rol(id)
);

-- menús (con función asociada)
CREATE TABLE menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    funcion TEXT NOT NULL
);

-- explotaciones
CREATE TABLE explotacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    ubicacion TEXT
);

-- parcelas
CREATE TABLE parcela (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    id_explotacion INTEGER NOT NULL,
    FOREIGN KEY (id_explotacion) REFERENCES explotacion(id)
);

-- sensores
CREATE TABLE sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    descripcion TEXT
);

-- mediciones
CREATE TABLE medicion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_parcela INTEGER NOT NULL,
    id_sensor INTEGER NOT NULL,
    valor REAL NOT NULL,
    fecha TEXT NOT NULL,
    FOREIGN KEY (id_parcela) REFERENCES parcela(id),
    FOREIGN KEY (id_sensor) REFERENCES sensor(id)
);

-- tratamientos
CREATE TABLE tratamiento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_parcela INTEGER NOT NULL,
    descripcion TEXT,
    fecha TEXT NOT NULL,
    confirmado BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_parcela) REFERENCES parcela(id)
);

-- análisis foliar o suelo
CREATE TABLE analisis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_parcela INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    resultado TEXT,
    fecha TEXT NOT NULL,
    FOREIGN KEY (id_parcela) REFERENCES parcela(id)
);

-- notificaciones
CREATE TABLE notificacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    mensaje TEXT NOT NULL,
    leida BOOLEAN DEFAULT 0,
    fecha TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

-- parámetros normales
CREATE TABLE parametro_normal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    variable TEXT NOT NULL,
    valor_min REAL,
    valor_max REAL
);

-- Datos iniciales
INSERT INTO rol (nombre) VALUES ('Administrador'), ('Técnico'), ('Consultor');

INSERT INTO usuario (nombre, email, password, id_rol)
VALUES
('Admin', 'admin@olivar.local', 'admin123', 1),
('Técnico Juan', 'juan@olivar.local', 'tecnico123', 2);

INSERT INTO menu (nombre, funcion) VALUES
('Gestión de Sensores', 'abrir_sensores'),
('Tratamientos', 'abrir_tratamientos'),
('Análisis', 'abrir_analisis');

INSERT INTO explotacion (nombre, ubicacion) VALUES
('Finca Los Olivos', 'Jaén'),
('Finca La Loma', 'Córdoba');

INSERT INTO parcela (nombre, id_explotacion) VALUES
('Parcela A', 1),
('Parcela B', 2);

INSERT INTO sensor (tipo, descripcion) VALUES
('temperatura', 'Sensor de temperatura de savia'),
('composición', 'Sensor de composición química de savia');

INSERT INTO parametro_normal (tipo, variable, valor_min, valor_max) VALUES
('savia', 'temperatura', 10.0, 35.0),
('savia', 'composición', 0.5, 2.0),
('suelo', 'nitrógeno', 0.1, 1.5),
('foliar', 'hierro', 30.0, 100.0);
