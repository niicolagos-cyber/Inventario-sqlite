use inventario;

-- Valor total del stock agrupado por categoría
SELECT categoria,
       SUM(precio * stock_actual) AS valor_total
FROM productos
GROUP BY categoria
ORDER BY valor_total DESC;