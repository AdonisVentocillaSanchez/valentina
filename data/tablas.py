import sqlite3

#Conexión con la base de datos
con = sqlite3.connect("Proyecto_Linio.db")

cursor =  con.cursor()

#Creación de tabla Usuario
cursor.execute("""
DROP TABLE IF EXISTS usuario;
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuario (
    codigo_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    primer_nombre TEXT NOT NULL,
    primer_apellido TEXT NOT NULL,
    segundo_apellido TEXT NOT NULL,
    edad INTEGER,
    correo_electronico TEXT NOT NULL,
    telefono INTEGER,
    nro_tarjeta_bancaria TEXT,
    nombre_usuario TEXT NOT NULL,
    contrasena TEXT NOT NULL)
    """)
con.commit()

#Creación de tabla Comercio
cursor.execute("""
DROP TABLE IF EXISTS comercio;
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS comercio (
    codigo_comercio INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    direccion TEXT NOT NULL,
    RUC INTEGER,
    contrasena TEXT NOT NULL)
    """)
con.commit()

#Creación de tabla Carrito
cursor.execute("""
DROP TABLE IF EXISTS carrito;
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS carrito (
    codigo_carrito INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_usuario INTEGER,
    precio_total DOUBLE,
    cantidad_producto INTEGER,
    status INTEGER)
    """)
con.commit()

#Creación de tabla Categoría
cursor.execute("""
DROP TABLE IF EXISTS categoria;
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS categoria (
    codigo_categoria INTEGER PRIMARY KEY,
    nombre STRING)
    """)
con.commit()

# Creación de tabla Pedido
cursor.execute("""
DROP TABLE IF EXISTS pedido;
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS pedido (
    codigo_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_usuario INTEGER,
    codigo_carrito INTEGER,
    estado STRING,
    repartidor STRING,
    tipo_comprobante STRING,
    metodo_pago STRING,
    direccion_envio STRING,
    area_reparto STRING,
    tarifa_envio DOUBLE,
    fecha_entrega DATETIME NOT NULL,
    fecha_emision DATETIME NOT NULL,
    FOREIGN KEY(codigo_usuario) REFERENCES usuario(codigo_usuario),
    FOREIGN KEY(codigo_carrito) REFERENCES carrito(codigo_carrito))""")
con.commit()

#Creación de tabla Producto
cursor.execute("""
DROP TABLE IF EXISTS producto;
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS producto (
    codigo_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_carrito INTEGER,
    codigo_categoria INTEGER,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    precio DOUBLE,
    tienda TEXT NOT NULL,
    stock INTEGER,
    FOREIGN KEY(codigo_carrito) REFERENCES carrito(codigo_carrito)
    FOREIGN KEY(codigo_categoria) REFERENCES categoria(codigo_categoria)
    )""")
con.commit()
 
#Creación de Tabla Ofrecer
cursor.execute("""
DROP TABLE IF EXISTS ofrecer;
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS ofrecer (
    codigo_ofrecer INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_comercio INTEGER,
    codigo_producto INTEGER,
    FOREIGN KEY (codigo_comercio) REFERENCES comercio(codigo_comercio),
    FOREIGN KEY (codigo_producto) REFERENCES producto(codigo_producto)
    )""")
con.commit()