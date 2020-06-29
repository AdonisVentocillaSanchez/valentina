import sqlite3

class IterableCategoria(type):
    def __iter__(cls):
        return iter(cls.__name__)

class Categoria(object):
    __metaclass__ = IterableCategoria
    def __init__(self, codigo_categoria:int=None, nombre:str=None):
        self.codigo_categoria = codigo_categoria
        self.nombre = nombre

    @property
    def codigo_categoria(self):
        return self.__codigo_categoria
    @codigo_categoria.setter
    def codigo_categoria(self, pcodigo_categoria):
        self.__codigo_categoria = pcodigo_categoria

    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, pnombre):
        self.__nombre = pnombre

    ## Funcion para buscar el nombre de una categoria
    def buscar(self, id:int) -> str:
        name = None
        try:
            database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                SELECT nombre FROM categoria where codigo_categoria={}'''.format(id)
            cursor.execute(query)
            name = cursor.fetchone()
            return name
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
            return name
