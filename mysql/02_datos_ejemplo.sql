USE inventario;

INSERT INTO productos (codigo, nombre, categoria, precio, stock_actual, stock_minimo) VALUES
('HUE001', 'Huevo líquido entero 1 kg',      'Líquidos', 3500.00, 50, 20),
('HUE002', 'Clara líquida pasteurizada 1 kg', 'Líquidos', 4200.00, 12, 15),
('HUE003', 'Yema líquida 1 kg',               'Líquidos', 4800.00, 30, 10),
('POL001', 'Huevo entero en polvo 500 g',     'Polvos',   9800.00, 25,  8),
('POL002', 'Clara en polvo 500 g',            'Polvos',  12500.00,  5,  5);

INSERT INTO movimientos (producto_id, tipo, cantidad, nota) VALUES
(1, 'ENTRADA', 60, 'Compra inicial'),
(2, 'ENTRADA', 12, 'Compra inicial'),
(3, 'ENTRADA', 30, 'Compra inicial'),
(4, 'ENTRADA', 25, 'Compra inicial'),
(5, 'ENTRADA',  5, 'Compra inicial'),
(1, 'SALIDA',  10, 'Pedido cliente');

USE inventario;
SELECT * FROM productos;
SELECT * FROM movimientos;