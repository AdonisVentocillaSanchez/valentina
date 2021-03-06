import sqlite3

class Comercio(object):
    def __init__(self, codigo_comercio:int=None, nombre:str=None, direccion:str=None, RUC:int=None, contrasena:str=None):
        self.codigo_comercio = codigo_comercio
        self.nombre = nombre
        self.direccion= direccion
        self.RUC = RUC
        self.contrasena = contrasena
        self.ListaProducto = []

    @property
    def codigo_comercio(self):
        return self.__codigo_comercio
    @codigo_comercio.setter
    def codigo_comercio(self, pcodigo_comercio):
        self.__codigo_comercio = pcodigo_comercio

    @property
    def nombre(self):
        return self.__nombre
    @codigo_comercio.setter
    def nombre(self, pnombre):
        self.__nombre = pnombre

    @property
    def direccion(self):
        return self.__direccion
    @direccion.setter
    def direccion(self, pdireccion):
        self.__direccion = pdireccion

    @property
    def RUC(self):
        return self.__RUC
    @RUC.setter
    def RUC(self, pRUC):
        self.__RUC = pRUC
    
    @property
    def contrasena(self):
        return self.__contrasena
    @contrasena.setter
    def contrasena(self, pcontrasena):
        self.__contrasena = pcontrasena

    @property
    def ListaProducto(self):
        return self.__ListaProducto
    @ListaProducto.setter
    def ListaProducto(self, pListaProducto):
        self.__ListaProducto = pListaProducto
    
    ## CREAR CUENTA COMERCIO
    def crear_cuenta(self) -> bool:
        estado_op = False
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            INSERT INTO comercio(nombre, direccion, RUC, contrasena)
            VALUES ('{}', '{}', {}, '{}')
            '''.format(self.__nombre, self.__direccion, self.__RUC, self.__contrasena)

            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY

            estado_op = True

        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return estado_op

    def obtener_comercio(self, ruc:str) :
        comercio=None
        try:
            database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                SELECT *
                FROM Comercio WHERE RUC= {}
                '''.format(ruc)

            cursor.execute(query)
            comercio = cursor.fetchone()
            print(comercio)
            comercioObj = Comercio(
                codigo_comercio=comercio[0],
                nombre=comercio[1],
                direccion=comercio[2],
                RUC=comercio[3],
                contrasena=comercio[4]
            )
            return comercioObj

        except Exception as e:
            print("Error: {}".format(e))
        finally:
            database.close()
            return comercio

    