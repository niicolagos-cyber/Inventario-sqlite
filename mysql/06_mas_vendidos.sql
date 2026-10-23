USE inventario;

-- Top 3 productos con más unidades en salidas
SELECT p.codigo,
       p.nombre,
       SUM(m.cantidad) AS unidades_vendidas
FROM productos p
JOIN movimientos m ON m.producto_id = p.id
WHERE m.tipo = 'SALIDA'
GROUP BY p.id, p.codigo, p.nombre
ORDER BY unidades_vendidas DESC
LIMIT 3;