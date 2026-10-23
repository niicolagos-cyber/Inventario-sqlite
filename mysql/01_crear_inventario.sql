CREATE DATABASE IF NOT EXISTS inventario CHARACTER SET utf8mb4;
USE inventario;

CREATE TABLE IF NOT EXISTS productos (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    codigo       VARCHAR(20)   NOT NULL UNIQUE,
    nombre       VARCHAR(100)  NOT NULL,
    categoria    VARCHAR(50)   NOT NULL DEFAULT 'General',
    precio       DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    stock_actual INT           NOT NULL DEFAULT 0 CHECK (stock_actual >= 0),
    stock_minimo INT           NOT NULL DEFAULT 0 CHECK (stock_minimo >= 0)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS movimientos (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT          NOT NULL,
    tipo        ENUM('ENTRADA','SALIDA') NOT NULL,
    cantidad    INT          NOT NULL CHECK (cantidad > 0),
    fecha       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nota        VARCHAR(255),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
) ENGINE=InnoDB;