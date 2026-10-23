USE inventario;

-- Valor del stock de cada producto, del más caro al más barato
SELECT nombre, precio * stock_actual AS valor
FROM productos
ORDER BY valor DESC;