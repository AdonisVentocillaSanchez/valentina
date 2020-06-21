import sqlite3

con = sqlite3.connect('Proyecto_Linio.db')
cursor = con.cursor()

# Inserta datos a la tabla usuario
cursor.execute("""
INSERT INTO usuario(primer_nombre, primer_apellido, segundo_apellido, edad, correo_electronico, telefono, nro_tarjeta_bancaria, nombre_usuario, contrasena)
    VALUES ('Berenice','Espinoza','Luna',20,'bere@gmail.com',982528765,'4551-0382-6988-3142','berenicedaiana', 'espinozaluna'),
    ('Karina','Blas','Fernandez',21,'kari@gmail.com',995295729,'4280-8200-9076-8206','karina','blasfernandez'),
    ('Valentina','Yangali','Torres',21,'valentina@gmail.com',943061178,'4219-1801-2039-5181','valentina','yangalitorres'),
    ('Sheila','Vera','Falcon',21,'sheila@gmail.com',940247734,'4474-3700-1030-3276','sheila','verafalcon'),
    ('Blanca','Chavez','Alvarado', 21, 'blanca@gmail.com',993463816,'4484-6424-2040-5383','blancaalexandra','chavezalvarado')
    """)
con.commit()

#Valida datos ingresados a la tabla usuario
cursor.execute('SELECT * FROM usuario')
rows = cursor.fetchall()
for row in rows:
    print(row)

#Inserta datos a la tabla carrito
cursor.execute("""
    INSERT INTO carrito (codigo_usuario, precio_total, cantidad_producto, status)
    VALUES (1,584.00,1,1),
    (2,70.00,1,1),
    (3,24.95,1,1),
    (4,10.00,1,1),
    (5,70.00,1,1)
    """)

#Valida datos ingresados a la tabla carrito
cursor.execute('SELECT * FROM carrito')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Inserta datos a la tabla comercio
cursor.execute("""
INSERT INTO comercio(nombre, direccion, RUC,contrasena)
    VALUES ('Xiaomi', 'Av. Inca Garcilaso de la Vega 1348', 20653734101,'123'),
    ('Lenovo','Av. Dionisio Derteano 144',20854363302,'123'),
    ('Diadora','Av. La Marina 34342', 20744325203,'123'),
    ('Miniso','Av.Javier Prado Este 4200',20633214104,'123'),
    ('OEM','Av. Javier Prado Este 996', 20789561007,'123')
    """)
con.commit()

#Valida datos ingresados a la tabla comercio
cursor.execute('SELECT * FROM comercio')
rows = cursor.fetchall()
for row in rows:
    print(row)

#Inserta datos a la tabla categoria
cursor.execute("""
INSERT INTO categoria(nombre)
    VALUES ('Arte y artesanias'),
    ('Computadoras'),
    ('Moda'),
    ('Belleza y cuidado personal'),
    ('Salud y Bienestar'),
    ('Deportes'),
    ('Juguetes'), 
    ('Electrodomesticos')
    """)
con.commit()

#Valida datos ingresados a la tabla categoria
cursor.execute('SELECT * FROM categoria')
rows = cursor.fetchall()
for row in rows:
    print(row)

#Inserta datos a la tabla producto
cursor.execute("""
INSERT INTO producto(codigo_carrito,codigo_categoria,nombre,descripcion,precio,tienda,stock)
    VALUES (1,1, 'reloj', 'reloj mecánico de mijo para mujer, artesanía ligera',584.00,'Xiaomi',45 ),
    (2,2, 'auricular', 'auricular inalámbrico Blueetooth impermeable de deporte, color blanco',70.00,'Lenovo',17),
    (3,3, 'polo', 'polo deportivo para mujer, color fucsia',24.95,'Diadora',60),
    (4,4, 'set de mascarillas','utensilios de Belleza', 10.00, 'Miniso',90),
    (5,5, 'masajeador','masajeador de cuello, lumbar, pierna y mano de 17 cm de longitud', 70.00, 'OEM', 21)
    """)
con.commit()

#Valida datos ingresados a la tabla producto
cursor.execute('SELECT * FROM producto')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Inserta datos a la tabla pedido
cursor.execute("""
INSERT INTO pedido(codigo_usuario, codigo_carrito, estado, repartidor, tipo_comprobante, metodo_pago, direccion_envio, area_reparto, tarifa_envio, fecha_entrega, fecha_emision)
    VALUES (1,1,'pago pendiente','Manuel','boleta','efectivo','Av. Los Patriotas 456','Zona Central>', 12.5, '10/06/2020','07/06/2020'),
    (2,2,'pagado','Carlos','factura','tarjeta','Av. Universitaria 2456','Zona Central',10, '23/06/2020','26/06/2020'),
    (3,3,'pago pendiente', 'Martin','boleta','efectivo','Av. Javier Prado Este 2320','Zona Central Sur',8,'30/06/2020','03/07/2020'),
    (4,4,'pagado','Maria', 'boleta', 'tarjeta','Jr. El Chaco 2520','Zona Norte',15,'02/07/2020','05/07/2020'),
    (5,5,'pago pendiente','Elisa','factura','efectivo','Av. La Molina 1506', 'Zona Este', 18,'15/06/2020','18/06/2020')
    """)
con.commit()

#Valida datos ingresados a la tabla pedido
cursor.execute('SELECT * FROM pedido')
rows = cursor.fetchall()
for row in rows:
    print(row)


#Inserta datos a la tabla ofrecer
cursor.execute("""
INSERT INTO ofrecer(codigo_comercio,codigo_producto)
    VALUES (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5)
    """)
con.commit()

#Valida datos ingresados a la tabla ofrecer
cursor.execute('SELECT * FROM ofrecer')
rows = cursor.fetchall()
for row in rows:
    print(row)
