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
