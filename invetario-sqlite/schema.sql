-- Esquema de la base de datos del inventario
-- Dos tablas: productos y movimientos (historial de entradas/salidas)

CREATE TABLE IF NOT EXISTS productos (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo        TEXT    NOT NULL UNIQUE,                       -- código único (ej: "HUE001")
    nombre        TEXT    NOT NULL,
    categoria     TEXT    NOT NULL DEFAULT 'General',
    precio        REAL    NOT NULL CHECK (precio >= 0),
    stock_actual  INTEGER NOT NULL DEFAULT 0 CHECK (stock_actual >= 0),  -- nunca negativo
    stock_minimo  INTEGER NOT NULL DEFAULT 0 CHECK (stock_minimo >= 0)   -- umbral de alerta
);

CREATE TABLE IF NOT EXISTS movimientos (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id  INTEGER NOT NULL REFERENCES productos(id),      -- clave foránea
    tipo         TEXT    NOT NULL CHECK (tipo IN ('ENTRADA', 'SALIDA')),
    cantidad     INTEGER NOT NULL CHECK (cantidad > 0),
    fecha        TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    nota         TEXT
);

-- Índice para que buscar el historial de un producto sea rápido
CREATE INDEX IF NOT EXISTS idx_movimientos_producto ON movimientos(producto_id);
