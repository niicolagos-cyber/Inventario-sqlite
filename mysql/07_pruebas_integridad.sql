USE inventario;

-- PRUEBAS DE INTEGRIDAD: cada sentencia de abajo DEBE dar error.
-- Si alguna se ejecuta sin error, hay una regla que no está funcionando.

-- 1. Stock negativo (viola CHECK stock_actual >= 0)
INSERT INTO productos (codigo, nombre, categoria, precio, stock_actual, stock_minimo)
VALUES ('TST001', 'Producto de prueba', 'Pruebas', 100.00, -5, 0);

-- 2. Código duplicado (viola UNIQUE en codigo)
INSERT INTO productos (codigo, nombre, categoria, precio, stock_actual, stock_minimo)
VALUES ('HUE001', 'Producto duplicado', 'Pruebas', 100.00, 10, 0);

-- 3. Precio negativo (viola CHECK precio >= 0)
INSERT INTO productos (codigo, nombre, categoria, precio, stock_actual, stock_minimo)
VALUES ('TST002', 'Precio negativo', 'Pruebas', -50.00, 10, 0);

-- 4. Movimiento de un producto que no existe (viola la clave foránea)
INSERT INTO movimientos (producto_id, tipo, cantidad, nota)
VALUES (999, 'ENTRADA', 10, 'Producto inexistente');

-- 5. Cantidad cero (viola CHECK cantidad > 0)
INSERT INTO movimientos (producto_id, tipo, cantidad, nota)
VALUES (1, 'ENTRADA', 0, 'Cantidad cero');

-- 6. Tipo de movimiento inválido (viola el ENUM)
INSERT INTO movimientos (producto_id, tipo, cantidad, nota)
VALUES (1, 'DEVOLUCION', 5, 'Tipo no permitido');

SELECT COUNT(*) AS productos FROM productos;
SELECT COUNT(*) AS movimientos FROM movimientos;