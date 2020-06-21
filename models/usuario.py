import sqlite3
 
class Usuario(object):

    def __init__(self, codigo_usuario:int=None, primer_nombre:str=None, primer_apellido:str=None,
                 segundo_apellido:str=None, edad:int=None, correo_electronico:str=None,
                 telefono:int=None, nro_tarjeta_bancaria:int=None, nombre_usuario:str=None,
                 contrasena:str=None):
        self.codigo_usuario = codigo_usuario
        self.primer_nombre = primer_nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.edad = edad
        self.correo_electronico = correo_electronico
        self.telefono = telefono
        self.nro_tarjeta_bancaria = nro_tarjeta_bancaria
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena

    @property
    def contrasena(self) -> str:
        return self.__contrasena

    @property
    def codigo_usuario(self) -> int:
        return self.__codigo_usuario

    @property
    def primer_nombre(self) -> str:
        return self.__primer_nombre

    @property
    def primer_apellido(self) -> str:
        return self.__primer_apellido

    @property
    def segundo_apellido(self) -> str:
        return self.__segundo_apellido

    @property
    def edad(self) -> int:
        return self.__edad

    @property
    def correo_electronico(self) -> str:
        return self.__correo_electronico

    @property
    def telefono(self) -> int:
        return self.__telefono

    @property
    def nro_tarjeta_bancaria(self) -> str:
        return self.__nro_tarjeta_bancaria

    @property
    def nombre_usuario(self) -> str:
        return self.__nombre_usuario

    @codigo_usuario.setter
    def codigo_usuario(self, pcodigo_usuario):
        self.__codigo_usuario = pcodigo_usuario

    @primer_nombre.setter
    def primer_nombre(self, pprimer_nombre):
        self.__primer_nombre = pprimer_nombre

    @primer_apellido.setter
    def primer_apellido(self, pprimer_apellido):
        self.__primer_apellido = pprimer_apellido

    @segundo_apellido.setter
    def segundo_apellido(self, psegundo_apellido):
        self.__segundo_apellido = psegundo_apellido

    @edad.setter
    def edad(self, pedad):
        self.__edad = pedad

    @correo_electronico.setter
    def correo_electronico(self, pcorreo_electronico):
        self.__correo_electronico = pcorreo_electronico

    @telefono.setter
    def telefono(self, ptelefono):
        self.__telefono = ptelefono

    @nro_tarjeta_bancaria.setter
    def nro_tarjeta_bancaria(self, pnro_tarjeta_bancaria):
        self.__nro_tarjeta_bancaria = pnro_tarjeta_bancaria

    @nombre_usuario.setter
    def nombre_usuario(self, pnombre_usuario):
        self.__nombre_usuario = pnombre_usuario

    @contrasena.setter
    def contrasena(self, pcontrasena):
        self.__contrasena = pcontrasena

    def crear_cuenta(self) -> bool:
        estado_op = False
        database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
        try:

            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
            INSERT INTO Usuario(primer_nombre, primer_apellido, segundo_apellido, edad, correo_electronico, telefono, nro_tarjeta_bancaria, nombre_usuario, contrasena)
            VALUES ('{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}')
            '''.format(self.__primer_nombre, self.__primer_apellido, self.__segundo_apellido, self.__edad, self.__correo_electronico, self.__telefono, self.__nro_tarjeta_bancaria, self.__nombre_usuario, self.__contrasena)

            cursor.execute(query)
            database.commit()  # CONFIRMAR CAMBIOS QUERY

            estado_op = True

        except Exception as e:
            database.rollback()  # RESTAURAR ANTES DE CAMBIOS POR ERROR
            print("Error: {}".format(e))
        finally:
            database.close()  # CERRAR CONEXION CON BASE DE DATOS

        return estado_op

    def obtener_usuario(self, correo_electronico:str):
        usuario=None
        try:
            database = sqlite3.connect("data/Proyecto_Linio.db")  # ABRIR CONEXION CON BASE DE DATOS
            cursor = database.cursor()  # OBTENER OBJETO CURSOR
            query = '''
                SELECT *
                FROM Usuario WHERE correo_electronico= '{}'
                '''.format(correo_electronico)

            cursor.execute(query)
            usuario = cursor.fetchone()

            user = Usuario(
                primer_nombre=usuario[1],
                primer_apellido=usuario[2],
                segundo_apellido=usuario[3],
                edad=usuario[4],
                correo_electronico=usuario[5],
                telefono=usuario[6],
                nro_tarjeta_bancaria=usuario[7],
                nombre_usuario=usuario[8],
                contrasena=usuario[9],
                codigo_usuario=usuario[0]
            )

        except Exception as e:
            print("Error: {}".format(e))
        finally:
                database.close()
        return user