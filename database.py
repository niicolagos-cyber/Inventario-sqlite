"""
database.py
Todo lo que habla con la base de datos SQLite vive acá.
main.py solo se ocupa del menú; nunca escribe SQL directamente.
"""

import sqlite3
from pathlib import Path

# Rutas relativas a esta carpeta, así funciona sin importar desde dónde lo ejecutes
CARPETA = Path(__file__).parent
DB_PATH = CARPETA / "inventario.db"
SCHEMA_PATH = CARPETA / "schema.sql"


def conectar():
    """Abre una conexión a la base y activa las claves foráneas."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acceder a las columnas por nombre: fila["nombre"]
    conn.execute("PRAGMA foreign_keys = ON")  # SQLite las trae desactivadas por defecto
    return conn


def inicializar_db():
    """Crea las tablas si todavía no existen (lee schema.sql)."""
    conn = conectar()
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------- PRODUCTOS

def agregar_producto(codigo, nombre, categoria, precio, stock_minimo):
    """Inserta un producto nuevo. Lanza ValueError si el código ya existe o los datos no son válidos."""
    conn = conectar()
    try:
        # Los "?" son parámetros: NUNCA armes el SQL concatenando strings (inyección SQL)
        conn.execute(
            "INSERT INTO productos (codigo, nombre, categoria, precio, stock_minimo) "
            "VALUES (?, ?, ?, ?, ?)",
            (codigo.upper(), nombre, categoria, precio, stock_minimo),
        )
        conn.commit()
    except sqlite3.IntegrityError as error:
        # Salta si se viola UNIQUE o algún CHECK del esquema
        raise ValueError(f"No se pudo agregar el producto: {error}")
    finally:
        conn.close()


def listar_productos():
    """Devuelve todos los productos ordenados por nombre."""
    conn = conectar()
    try:
        return conn.execute("SELECT * FROM productos ORDER BY nombre").fetchall()
    finally:
        conn.close()


def buscar_productos(texto):
    """Busca productos cuyo nombre, código o categoría contengan el texto."""
    conn = conectar()
    try:
        patron = f"%{texto}%"
        return conn.execute(
            "SELECT * FROM productos "
            "WHERE nombre LIKE ? OR codigo LIKE ? OR categoria LIKE ? "
            "ORDER BY nombre",
            (patron, patron, patron),
        ).fetchall()
    finally:
        conn.close()


def productos_bajo_stock():
    """Productos cuyo stock actual está en el mínimo o por debajo."""
    conn = conectar()
    try:
        return conn.execute(
            "SELECT * FROM productos WHERE stock_actual <= stock_minimo ORDER BY stock_actual"
        ).fetchall()
    finally:
        conn.close()


# -------------------------------------------------------------- MOVIMIENTOS

def registrar_movimiento(codigo, tipo, cantidad, nota=""):
    """
    Registra una ENTRADA o SALIDA de stock.
    Hace dos cosas juntas: actualiza el stock Y guarda el movimiento.
    Si algo falla, no se guarda ninguna de las dos (transacción).
    """
    tipo = tipo.upper()
    if tipo not in ("ENTRADA", "SALIDA"):
        raise ValueError("El tipo debe ser ENTRADA o SALIDA.")
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a cero.")

    conn = conectar()
    try:
        producto = conn.execute(
            "SELECT id, stock_actual FROM productos WHERE codigo = ?", (codigo.upper(),)
        ).fetchone()
        if producto is None:
            raise ValueError(f"No existe ningún producto con el código {codigo.upper()}.")

        if tipo == "SALIDA" and cantidad > producto["stock_actual"]:
            raise ValueError(
                f"Stock insuficiente: hay {producto['stock_actual']} y querés sacar {cantidad}."
            )

        # Si es entrada suma, si es salida resta
        delta = cantidad if tipo == "ENTRADA" else -cantidad

        conn.execute(
            "UPDATE productos SET stock_actual = stock_actual + ? WHERE id = ?",
            (delta, producto["id"]),
        )
        conn.execute(
            "INSERT INTO movimientos (producto_id, tipo, cantidad, nota) VALUES (?, ?, ?, ?)",
            (producto["id"], tipo, cantidad, nota),
        )
        conn.commit()  # recién acá se guardan los dos cambios
    except Exception:
        conn.rollback()  # si algo falló, se deshace todo
        raise
    finally:
        conn.close()


def historial_producto(codigo):
    """Devuelve los movimientos de un producto, del más nuevo al más viejo."""
    conn = conectar()
    try:
        # JOIN: une cada movimiento con los datos de su producto
        return conn.execute(
            "SELECT m.fecha, m.tipo, m.cantidad, m.nota, p.nombre "
            "FROM movimientos m "
            "JOIN productos p ON p.id = m.producto_id "
            "WHERE p.codigo = ? "
            "ORDER BY m.fecha DESC, m.id DESC",
            (codigo.upper(),),
        ).fetchall()
    finally:
        conn.close()
