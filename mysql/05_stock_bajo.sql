USE inventario;

-- Productos que llegaron al stock mínimo o están por debajo
SELECT codigo, nombre, stock_actual, stock_minimo
FROM productos
WHERE stock_actual <= stock_minimo
ORDER BY stock_actual;