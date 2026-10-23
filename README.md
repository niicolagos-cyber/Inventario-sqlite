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
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
## Versión MySQL

El mismo inventario, implementado en MySQL. Los scripts están en la carpeta `mysql/`.

| Archivo | Qué hace |
| --- | --- |
| `01_crear_inventario.sql` | Crea la base `inventario` y las tablas `productos` y `movimientos` |
| `02_datos_ejemplo.sql` | Carga 5 productos y sus movimientos de ejemplo |
| `03_valor_inventario.sql` | Valor del stock de cada producto |
| `04_valor_por_categoria.sql` | Valor total agrupado por categoría (`GROUP BY`) |
| `05_stock_bajo.sql` | Productos en o por debajo del stock mínimo |
| `06_mas_vendidos.sql` | Top 3 de productos con más salidas (`JOIN`) |
| `07_pruebas_integridad.sql` | Inserciones inválidas que deben fallar |

### Cómo usarlo

1. Ejecutar `01_crear_inventario.sql` y después `02_datos_ejemplo.sql`.
2. Ejecutar cualquiera de las consultas (`03` a `06`).

### Pruebas de integridad

El archivo `07` verifica que la base rechaza datos incorrectos: stock o
precio negativos, códigos duplicados, movimientos de productos inexistentes,
cantidades en cero y tipos de movimiento inválidos. Cada sentencia debe
devolver un error; los conteos de filas se verifican después para
confirmar que no se guardó ningún dato inválido.