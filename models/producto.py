import sqlite3

class IterableProducto(type):
    def __iter__(cls):
        return iter(cls.__name__)

class Producto(object):
    __metaclass__ = IterableProducto
    def __init__(self, codigo_producto:int=None, nombre:str=None, descripcion:str=None,codigo_categoria:int=None,
                 precio:int=None, tienda:str=None, stock:int=None):
        self.codigo_producto= codigo_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio= precio
        self.tienda= tienda
        self.stock= stock
        self.codigo_categoria = codigo_categoria
        self.ListaCarrito = []
        self.ListaComercio = []
        self.ListaCategoria = []

    @property
    def codigo_producto(self) -> int:
        return self.__codigo_producto
    @codigo_producto.setter
    def codigo_producto(self, pcodigo_producto):
        self.__codigo_producto = pcodigo_producto

    @property
    def nombre(self) -> str:
        return self.__nombre
    @nombre.setter
    def nombre(self, pnombre):
        self.__nombre = pnombre

    @property
    def descripcion(self) -> str:
        return self.__descripcion
    @descripcion.setter
    def descripcion(self, pdescripcion):
        self.__descripcion = pdescripcion

    @property
    def precio(self) -> int:
        return self.__precio
    @precio.setter
    def precio(self, pprecio):
        self.__precio = pprecio

    @property
    def tienda(self) -> str:
        return self.__tienda
    @tienda.setter
    def tienda(self, ptienda):
        self.__tienda = ptienda

    @property
    def stock(self) -> int:
        return self.__stock
    @stock.setter
    def stock(self, pstock):
        self.__stock = pstock

    @property
    def ListaCarrito(self):
        return self.__ListaCarrito
    @ListaCarrito.setter
    def ListaCarrito(self, pListaCarrito):
        self.__ListaCarrito = pListaCarrito

    @property
    def ListaComercio(self):
        return self.__ListaComercio
    @ListaComercio.setter
    def ListaComercio(self, pListaComercio):
        self.__ListaComercio = pListaComercio

    @property
    def ListaCategoria(self):
        return self.__ListaCategoria
    @ListaCategoria.setter
    def ListaCategoria(self, pListaCategoria):
        self.__ListaCategoria = pListaCategoria

    @property
    def codigo_categoria(self) -> int:
        return self.__codigo_categoria

    @codigo_producto.setter
    def codigo_categoria(self, pcodigo_categoria):
        self.__codigo_categoria = pcodigo_categoria

    #Funcion para generar un codigo para el siguiente registro de producto
    def generar_codigo(self) -> int:
        count = 0
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            SELECT COUNT(*) FROM producto'''
            cursor.execute(query)
            count = cursor.fetchone()
            count = int(count[0])
            count = count + 1
        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return count

    #Funcion para añadir un producto
    def agregar_producto(self) -> bool:
        estado_op = False
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            cod = self.generar_codigo()
            query = '''
                INSERT INTO producto(codigo_producto, codigo_categoria, nombre, descripcion, precio, tienda, stock)
                        VALUES ({}, {}, '{}', '{}', {}, '{}', {})
                        '''.format(cod, self.__codigo_categoria,self.__nombre, self.__descripcion, self.__precio, self.__tienda,self.__stock)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return estado_op

    #Funcion para buscar todos los productos
    def buscar_productos(self):
        producto = None
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                SELECT * FROM Producto '''
            cursor.execute(query)
            producto= cursor.fetchone()
            database.commit()  # CONFIRMAR CAMBIOS QUERY
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return producto
    
    #Buscar un solo producto
    def buscar_producto(self, idprod:int):
        producto = None
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                SELECT * FROM Producto WHERE codigo_producto={}'''.format(idprod)
            cursor.execute(query)
            producto= cursor.fetchone()
            return producto
            database.commit()  # CONFIRMAR CAMBIOS QUERY
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return producto
    
    ## Buscar los productos por cada categoria
    def buscar_productos_categoria(self, id_categoria:int):
        list = None
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                SELECT * FROM producto where codigo_categoria={}'''.format(id_categoria)
            cursor.execute(query)
            list = cursor.fetchall()

            estado_op = True

            return list
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
            return list
    
    #Busca producto por palabra segun la categoria
    def buscar_producto_categoria(self, palabra:str, id_categoria:int):
        list = None
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                SELECT * FROM producto where codigo_categoria={} AND nombre LIKE '%{}%' '''.format(id_categoria, palabra)
            cursor.execute(query)
            list = cursor.fetchall()

            estado_op = True

            return list
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
    
    #Actualizar stock de un producto
    def actualizar_producto_stock(self, id_prod:int) -> bool:
        estado_op = False
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                UPDATE producto SET stock=stock-1 
                WHERE codigo_producto={} '''.format(id_prod)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_op = True

            return estado_op
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS


#SELECT codigo_producto,nombre,descripcion,precio,tienda,stock FROM producto