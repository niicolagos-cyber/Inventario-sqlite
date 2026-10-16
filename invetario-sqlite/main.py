"""
main.py
Menú de consola del inventario. Ejecutar con:  python main.py
"""

import database as db


# ------------------------------------------------------------------ AYUDAS

def pedir_texto(mensaje):
    """Pide un texto que no puede quedar vacío."""
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  El valor no puede estar vacío.")


def pedir_entero(mensaje, minimo=0):
    """Pide un número entero mayor o igual a 'minimo'."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor >= minimo:
                return valor
            print(f"  Tiene que ser {minimo} o más.")
        except ValueError:
            print("  Ingresá un número entero válido.")


def pedir_decimal(mensaje):
    """Pide un número decimal mayor o igual a cero (acepta coma o punto)."""
    while True:
        try:
            valor = float(input(mensaje).replace(",", "."))
            if valor >= 0:
                return valor
            print("  No puede ser negativo.")
        except ValueError:
            print("  Ingresá un número válido.")


def mostrar_tabla(productos):
    """Imprime una lista de productos en forma de tabla."""
    if not productos:
        print("\n  (No hay productos para mostrar)")
        return
    print(f"\n{'CÓDIGO':<10}{'NOMBRE':<25}{'CATEGORÍA':<15}{'PRECIO':>10}{'STOCK':>8}{'MÍN.':>7}")
    print("-" * 75)
    for p in productos:
        alerta = " !" if p["stock_actual"] <= p["stock_minimo"] else ""
        print(
            f"{p['codigo']:<10}{p['nombre'][:23]:<25}{p['categoria'][:13]:<15}"
            f"{p['precio']:>10.2f}{p['stock_actual']:>8}{p['stock_minimo']:>7}{alerta}"
        )


# ----------------------------------------------------------------- ACCIONES

def accion_agregar():
    print("\n--- Agregar producto ---")
    codigo = pedir_texto("Código (ej: HUE001): ")
    nombre = pedir_texto("Nombre: ")
    categoria = input("Categoría (Enter = General): ").strip() or "General"
    precio = pedir_decimal("Precio: ")
    stock_minimo = pedir_entero("Stock mínimo de alerta: ")
    try:
        db.agregar_producto(codigo, nombre, categoria, precio, stock_minimo)
        print("  Producto agregado.")
    except ValueError as error:
        print(f"  Error: {error}")


def accion_listar():
    print("\n--- Todos los productos ---")
    mostrar_tabla(db.listar_productos())


def accion_buscar():
    print("\n--- Buscar producto ---")
    texto = pedir_texto("Texto a buscar (nombre, código o categoría): ")
    mostrar_tabla(db.buscar_productos(texto))


def accion_movimiento(tipo):
    print(f"\n--- Registrar {tipo.lower()} ---")
    codigo = pedir_texto("Código del producto: ")
    cantidad = pedir_entero("Cantidad: ", minimo=1)
    nota = input("Nota (opcional): ").strip()
    try:
        db.registrar_movimiento(codigo, tipo, cantidad, nota)
        print(f"  {tipo.capitalize()} registrada.")
    except ValueError as error:
        print(f"  Error: {error}")


def accion_bajo_stock():
    print("\n--- Productos con stock bajo (marcados con !) ---")
    mostrar_tabla(db.productos_bajo_stock())


def accion_historial():
    print("\n--- Historial de un producto ---")
    codigo = pedir_texto("Código del producto: ")
    movimientos = db.historial_producto(codigo)
    if not movimientos:
        print("  No hay movimientos para ese código.")
        return
    print(f"\nProducto: {movimientos[0]['nombre']}")
    print(f"{'FECHA':<22}{'TIPO':<10}{'CANT.':>7}  NOTA")
    print("-" * 60)
    for m in movimientos:
        print(f"{m['fecha']:<22}{m['tipo']:<10}{m['cantidad']:>7}  {m['nota'] or ''}")


# --------------------------------------------------------------------- MENÚ

MENU = """
========== INVENTARIO ==========
1. Agregar producto
2. Listar productos
3. Buscar producto
4. Registrar entrada de stock
5. Registrar salida de stock
6. Ver productos con stock bajo
7. Ver historial de un producto
0. Salir
================================"""


def main():
    db.inicializar_db()  # crea las tablas la primera vez
    while True:
        print(MENU)
        opcion = input("Elegí una opción: ").strip()
        if opcion == "1":
            accion_agregar()
        elif opcion == "2":
            accion_listar()
        elif opcion == "3":
            accion_buscar()
        elif opcion == "4":
            accion_movimiento("ENTRADA")
        elif opcion == "5":
            accion_movimiento("SALIDA")
        elif opcion == "6":
            accion_bajo_stock()
        elif opcion == "7":
            accion_historial()
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("  Opción no válida.")


if __name__ == "__main__":
    main()
