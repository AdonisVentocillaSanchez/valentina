from datetime import datetime
from models.carrito import Carrito
import sqlite3
import datetime

class Pedido(object):
    def __init__(self, codigo_pedido:int=None, estado:str=None, repartidor:str=None,
                 tipo_comprobante:str=None, metodo_pago:str=None, direccion_envio:str=None,
                 area_reparto:str=None, tarifa_envio:int=None, fecha_entrega:datetime= None,
                 fecha_emision:datetime=None):
        self.codigo_pedido= codigo_pedido
        self.estado = estado
        self.repartidor = repartidor
        self.tipo_comprobante = tipo_comprobante
        self.metodo_pago = metodo_pago
        self.direccion_envio= direccion_envio
        self.area_reparto = area_reparto
        self.tarifa_envio= tarifa_envio
        self.fecha_entrega= fecha_entrega
        self.fecha_emision = fecha_emision
        self.oCarrito = Carrito()
        self.ListaUsuario = []

    @property
    def codigo_pedido(self):
        return self.__codigo_pedido
    @codigo_pedido.setter
    def codigo_pedido(self, pcodigo_pedido):
        self.__codigo_pedido = pcodigo_pedido

    @property
    def estado(self):
        return self.__estado
    @estado.setter
    def estado(self, pestado):
        self.__estado = pestado

    @property
    def repartidor(self):
        return self.__repartidor
    @repartidor.setter
    def repartidor(self, prepartidor):
        self.__repartidor = prepartidor

    @property
    def tipo_comprobante(self):
        return self.__tipo_comprobante
    @tipo_comprobante.setter
    def tipo_comprobante(self, ptipo_comprobante):
        self.__tipo_comprobante = ptipo_comprobante

    @property
    def metodo_pago(self):
        return self.__metodo_pago
    @metodo_pago.setter
    def metodo_pago(self, pmetodo_pago):
        self.__metodo_pago = pmetodo_pago

    @property
    def direccion_envio(self):
        return self.__direccion_envio
    @direccion_envio.setter
    def direccion_envio(self, pdireccion_envio):
        self.__direccion_envio = pdireccion_envio

    @property
    def area_reparto(self):
        return self.__area_reparto
    @area_reparto.setter
    def area_reparto(self, parea_reparto):
        self.__area_reparto = parea_reparto

    @property
    def tarifa_envio(self):
        return self.__tarifa_envio
    @tarifa_envio.setter
    def tarifa_envio(self, ptarifa_envio):
        self.__tarifa_envio = ptarifa_envio

    @property
    def fecha_entrega(self):
        return self.__fecha_entrega
    @fecha_entrega.setter
    def fecha_entrega(self, pfecha_entrega):
        self.__fecha_entrega = pfecha_entrega

    @property
    def fecha_emision(self):
        return self.__fecha_emision
    @fecha_emision.setter
    def fecha_emision(self, pfecha_emision):
        self.__fecha_emision = pfecha_emision

    @property
    def ListaUsuario(self):
        return self.__ListaUsuario
    @ListaUsuario.setter
    def ListaUsuario(self, pListaUsuario):
        self.__ListaUsuario = pListaUsuario

    #Funcion para añadir un pedido
    def generar(self, id_cart:int, id_user:int) -> bool:
        estado_op = False
        cartid = id_cart
        try:
            database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                INSERT INTO pedido(codigo_usuario, codigo_carrito, estado, repartidor, tipo_comprobante, metodo_pago, direccion_envio, area_reparto, tarifa_envio, fecha_entrega, fecha_emision)
                        VALUES ({}, {}, '{}', '{}', '{}', '{}','{}','{}',{}, '{}', '{}')
                        '''.format(cartid, id_cart, self.__estado,self.__repartidor, self.__tipo_comprobante, self.__metodo_pago, self.__direccion_envio,self.__area_reparto, self.__tarifa_envio, self.fecha_entrega, self.fecha_emision)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return estado_op
    
    #Buscar los pedidos de un solo usuario
    def listarpedido(self, idprod:int):
        producto = None
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                SELECT * FROM pedido WHERE codigo_usuario={} '''.format(idprod)
            cursor.execute(query)
            producto= cursor.fetchall()
            return producto
            database.commit()  # CONFIRMAR CAMBIOS QUERY
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
            return producto
    
    #Funcion para CANCELAR PEDIDO
    def cancelarpedido(self, id_ped:int) -> bool:
        estado_op = False
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                UPDATE pedido SET estado='cancelado'
                        WHERE codigo_pedido = {}
                        '''.format(id_ped)
            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY
            estado_op = True
        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS
            return estado_op

    