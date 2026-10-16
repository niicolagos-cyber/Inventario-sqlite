# Inventario con SQLite y Python

Aplicación de consola para gestionar el stock de productos, con historial de
entradas y salidas. Usa solo la librería estándar de Python (`sqlite3`), sin
dependencias externas.

## Funciones

- Alta de productos con código único, categoría, precio y stock mínimo
- Registro de entradas y salidas de stock (con nota opcional)
- Búsqueda por nombre, código o categoría
- Alerta de productos con stock bajo
- Historial de movimientos por producto

## Modelo de datos

```
productos                         movimientos
---------                         -----------
id (PK)                           id (PK)
codigo (UNIQUE)                   producto_id (FK -> productos.id)
nombre                            tipo (ENTRADA | SALIDA)
categoria                         cantidad (> 0)
precio (>= 0)                     fecha
stock_actual (>= 0)               nota
stock_minimo (>= 0)
```

Las reglas de integridad (stock nunca negativo, código único, cantidad mayor a
cero, claves foráneas) están definidas en `schema.sql` mediante `CHECK`,
`UNIQUE` y `REFERENCES`.

## Cómo ejecutarlo

Requiere Python 3.8 o superior.

```bash
python main.py
```

La base `inventario.db` se crea automáticamente la primera vez.

## Estructura

| Archivo        | Qué hace                                         |
| -------------- | ------------------------------------------------ |
| `schema.sql`   | Definición de tablas, restricciones e índice     |
| `database.py`  | Todas las consultas SQL (capa de acceso a datos) |
| `main.py`      | Menú de consola e interacción con el usuario     |

## Conceptos aplicados

- Consultas parametrizadas (previenen inyección SQL)
- Transacciones: actualizar stock y guardar el movimiento ocurre junto o no ocurre
- `JOIN` entre productos y movimientos
- Índices y restricciones de integridad

## Próximos pasos

- Tests con `pytest` para verificar las reglas de integridad
- Exportar reportes a CSV
- Migrar a PostgreSQL con Docker
