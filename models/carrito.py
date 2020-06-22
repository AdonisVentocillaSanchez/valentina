import sqlite3

class Carrito(object):
    def __init__(self, codigo_carrito:int=None, codigo_usuario:int=None, precio_total:int=None, cantidad_producto:int=None, status:int=None,):
        self.__codigo_carrito = codigo_carrito
        self.__codigo_usuario = codigo_usuario
        self.__precio_total = precio_total
        self.__cantidad_producto= cantidad_producto
        self.__status= status


    @property
    def codigo_carrito(self):
        return self.__codigo_carrito
    @codigo_carrito.setter
    def codigo_carrito(self, pcodigo_carrito):
        self.__codigo_carrito = pcodigo_carrito
    
    @property
    def codigo_usuario(self):
        return self.__codigo_usuario
    @codigo_usuario.setter
    def codigo_usuario(self, pcodigo_usuario):
        self.__codigo_usuario = pcodigo_usuario

    @property
    def precio_total(self): 
        return self.__precio_total
    @precio_total.setter
    def precio_total(self, pprecio_total):
        self.__precio_total = pprecio_total

    @property
    def cantidad_producto(self):
        return self.__cantidad_producto
    @cantidad_producto.setter
    def cantidad_producto(self, pcantidad_producto):
        self.__cantidad_producto = pcantidad_producto

    #Añadir pedido
    def agregar(self, cod_usu:int, precio:int) -> bool:
        estado_op = False
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            #Primero verificamos si el usuario tiene algun registro con status activo(1) en su carrito
            cursor1 = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                SELECT * FROM carrito where codigo_usuario={} AND status=1'''.format(cod_usu)
            cursor1.execute(query)
            result = cursor1.fetchall()
            

            if not result:
            #Si no cuenta con algun registro, creamos uno nuevo
                cursor2 = database.cursor()  # OBTENER OBJETO CURSOR
                query = '''
                INSERT INTO carrito(codigo_usuario, precio_total, cantidad_producto, status)
                        VALUES ('{}','{}', 1, 1)
                        '''.format(cod_usu, precio)
                cursor2.execute(query)
                database.commit()  # CONFIRMAR CAMBIOS QUERY
                estado_op = True
            else:
                #Si ya cuenta con su registro, actualiamos los datos
                cursor3 = database.cursor()  # OBTENER OBJETO CURSOR
                query = '''
                UPDATE carrito SET precio_total=precio_total + {} , cantidad_producto=cantidad_producto+1 
                        WHERE codigo_usuario = '{}'
                        '''.format(precio, cod_usu)
                cursor3.execute(query)
                database.commit()  # CONFIRMAR CAMBIOS QUERY
                estado_op = True

        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

            return estado_op

    #Buscar los productos por cada categoria
    def listar_carrito(self, id_user:int):
        list = None
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                SELECT * FROM carrito where codigo_usuario={} AND status=1'''.format(id_user)
            cursor.execute(query)
            list = cursor.fetchall()
            return list
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

    #Funcion para cambiar de estado el carrito
    def cambiar_estado_carrito(self, id_user:int) -> bool:
        estado_op = False
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                UPDATE carrito SET status=0 
                        WHERE codigo_carrito = '{}'
                        '''.format(id_user)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
            return estado_op
