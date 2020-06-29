from functools import wraps
from flask import Flask, render_template, request, redirect, session
from models.usuario import Usuario
from models.producto import Producto
from models.comercio import Comercio
from models.pedido import Pedido
from models.carrito import Carrito
from models.categoria import Categoria
from datetime import datetime as dt


app = Flask(__name__)

#Importacion de Clases
#Es necesario la importacion declarandolo de esta manera para 
#omitir las variables 'self' en las funciones dentro de la clase
Cusuario    = Usuario()
Cproducto   = Producto()
Ccomercio   = Comercio()
Cpedido      = Pedido()
Ccarrito     = Carrito()
Ccategoria   = Categoria()


#Primera ruta a ejecutarse en la pagina
@app.route('/')
def home():
    return render_template('home.html')

#Ruta de registro de usuarios
@app.route('/registro', methods=["get","post"])
def registration():
    if request.method == "POST":
        userprimernombre = request.form["primer_nombre"]
        userprimerapellido = request.form["primer_apellido"]
        usersegundoapellido = request.form["segundo_apellido"]
        useredad = request.form["edad"]
        usercorreoelectronico = request.form["correo_electronico"]
        usertelefono = request.form["telefono"]
        usernrotarjetabancaria = request.form["nro_tarjeta_bancaria"]
        usernombreusuario = request.form["nombre_usuario"]
        usercontrasena = request.form["contrasena"]

        usertelefono = int(usertelefono)
        useredad = int(useredad)

        user = Usuario(
            primer_nombre=userprimernombre,
            primer_apellido=userprimerapellido,
            segundo_apellido=usersegundoapellido,
            edad=useredad,
            correo_electronico=usercorreoelectronico,
            telefono=usertelefono,
            nro_tarjeta_bancaria= usernrotarjetabancaria,
            nombre_usuario=usernombreusuario,
            contrasena=usercontrasena
        )

        estado_op = user.crear_cuenta()

        if estado_op:
            return redirect("inicio-sesion")
        else:
            error = 'Invalid email'
            return render_template('users/register.html', error=error)
    return render_template('users/register.html')

#Ruta de registro de usuarios
@app.route('/registroC', methods=["get","post"])
def registrationC():
    if request.method == "POST":
        comerciouser = request.form["nombre"]
        comerciodireccion = request.form["direccion"]
        comercioRUC = int(request.form["ruc"])
        comerciocontrasena = request.form["contrasena"]

        ## Verificamos que el ruc sea igual a 11
        if len(str(comercioRUC))==11:
            ## Verificamos que no haya otro RUC igual registrado
            otroCom = Ccomercio.obtener_comercio(ruc=comercioRUC)
            if otroCom:
                error = 'El RUC ya está registrado'
                return render_template('comercio/register.html', error=error)
            else:
                newcomercio = Comercio(
                    nombre= comerciouser,
                    direccion= comerciodireccion,
                    RUC=comercioRUC,
                    contrasena=comerciocontrasena
                )
                estado_op = newcomercio.crear_cuenta()
                if estado_op:
                    return redirect("inicio-sesion-comercio")
                else:
                    error = 'Verifica tus datos'
                    return render_template('comercio/register.html', error=error)
        else:
            error = 'Verifique su RUC, debe tener 11 dígitos'
            return render_template('comercio/register.html', error=error)
    return render_template('comercio/register.html')
 
#Ruta para logueo de usuarios
@app.route('/inicio-sesion', methods=["get","post"])
def login():
    if request.method == "POST":
        correo_electronico=request.form["email"]
        ## Traer usuario con el correo
        user = Cusuario.obtener_usuario(correo_electronico = correo_electronico)

        if request.form["password"] == user.contrasena:
            session['user_id'] = user.codigo_usuario
            session['user_name'] = user.primer_nombre
            session['user_email'] = user.correo_electronico
            session['type'] = 1
            return redirect("/")
        else:
            error = 'Invalid password'
            return render_template('users/login.html', error=error)

    return render_template('users/login.html')

#Ruta para logueo de comercios
@app.route('/inicio-sesion-comercio', methods=["get","post"])
def loginComercio():
    if request.method == "POST":
        ruc=request.form["ruc"]
        comercio = Ccomercio.obtener_comercio(ruc=ruc)
        if comercio:
            ## comercio[4] es la contraseña
            if request.form["password"] == comercio[4]:
                ##comercio[3] es el RUC
                session['user_name'] = comercio[3]
                ##comercio[1] es el nombre de tienda
                session['user_tienda'] = comercio[1]
                session['type'] = 2
                return redirect("/")
            else:
                error = 'Invalid password'
                return render_template('comercio/login.html', error=error)
        else:
            error = 'Invalid RUC'
            return render_template('comercio/login.html', error=error)
    return render_template('comercio/login.html')

#Funcion para requerir un inicio de sesion
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        dat = None
        if 'user_name' in session:
            dat = session['user_name']
        if dat == None:
            return redirect('/inicio-sesion')
        return f(*args, **kwargs)
    return decorated_function

#Funcion para verificar logueo de Comercio que es type 2, sino va a login de comercio
def comercio_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        dat = 0
        if 'type' in session:
            dat = session['type']
        if dat != 2:
            return redirect('inicio-sesion-comercio')
        return f(*args, **kwargs)
    return decorated_function

#Ruta para cerrar sesion siempre y cuando se haya iniciado sesion
@app.route('/logout')
@login_required
def logout():
    session['user_name'] = None
    session['user_email'] = None
    session['type'] = None
    return redirect("/")

#Ruta para Registrar un producto SOLO para Comercios
@app.route('/registroProducto', methods=["get","post"])
@comercio_required
def registrarProducto():
    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = int(request.form["categoria"])
        descripcion = request.form["descripcion"]
        precio = int(request.form["precio"])
        tienda = request.form["tienda"]
        stock = int(request.form["stock"])

        produc = Producto(
            nombre=nombre,
            codigo_categoria=categoria,
            descripcion=descripcion,
            precio=precio,
            tienda=tienda,
            stock=stock
        )
        estado_op = produc.agregar_producto()

        if produc:
            error = 'PRODUCTO REGISTRADO'
            return render_template('users/registerProduct.html', error=error)
        else:
            error = 'Verifique los datos'
            return render_template('users/registerProduct.html', error=error)

    return render_template('users/registerProduct.html')

#Ruta para listar todos los productos
@app.route('/productos')
def products():
    product_list = Cproducto.buscar_productos()
    return render_template("users/products_list.html", product_list=product_list)


#Ruta para listar un producto
@app.route('/producto/<id_producto>')
def product_detail(id_producto):
    idProducto = int(id_producto)
    product = Cproducto.buscar_producto(idProducto)
    return render_template("product_detail.html", product=product)

#Ruta para listar productos segun la categoria y buscador segun nombre dentro de la categoria
@app.route('/productoCategoria/<id_categoria>', methods=["get","post"])
def product_category(id_categoria):
    idCategoria = int(id_categoria)
    nombreCategoria = Ccategoria.buscar(id=idCategoria)
    product_list = Cproducto.buscar_productos_categoria(idCategoria)

    if request.method == "POST":
        nombre = request.form["search"]

        product = Cproducto.buscar_producto_categoria(nombre, idCategoria)

        if not product:
            error = "Producto no encontrado"
            return render_template("users/products_list.html",product_list=product, error = error)
        else:
            return render_template("users/products_list.html",product_list=product)

    return render_template("users/products_list.html",product_list=product_list, categoria=nombreCategoria)

#Ruta para añadir al carrito un producto
@app.route('/addcarrito/<id_producto>')
@login_required
def add_cart(id_producto):
    idProducto = int(id_producto)
    product = Cproducto.buscar_producto(idprod= idProducto)
    id_user = session["user_id"]
    #Capturamos el precio segun la posicion que se encuentra en la base de datos
    precio_prod = product[5]
    #Capturamos el stock segun la posicion que se encuentra en la base de datos
    stock = product[7]
    #Verificamos que el stock sea mayor a 0 para agregar el producto al carrito
    if stock>0:
        #Agregamos el producto al carrito
        cartpe = Ccarrito.agregar(cod_usu=id_user, precio=precio_prod)
        #Verificamos que si se haya añadido
        if cartpe:
            Cproducto.actualizar_producto_stock(id_prod=idProducto)
            return render_template("users/products_list.html",message = "Producto agregado al carrito")
        else:
            # Sino se ha añadido mostramos un mensaje
            return render_template("users/products_list.html",message = "No se ha podido añadir el producto a tu carrito")
    else:
        return render_template("users/products_list.html",message = "No hay stock disponible")
    
    return render_template("users/products_list.html")
    

#Ruta para listar un el carrito de compras
@app.route('/carrito')
@login_required
def view_cart():
    idUser = session["user_id"]
    carrito = Ccarrito.listar_carrito(id_user=idUser)
    return render_template("users/carrito_detail.html", product=carrito)

#Ruta para listar un el carrito de compras
@app.route('/deletecarrito')
@login_required
def delete_cart():
    idUser = session["user_id"]
    carrito = Ccarrito.borrar_carrito(iduser= idUser)
    if carrito:
        message = "Carrito eliminado"
        return render_template("users/carrito_detail.html", error=message)


#Ruta para realizar un pedido a partir del carrito de compras
@app.route('/pedido', methods=["get","post"])
@login_required
def registrarPedido():
    carritoid = None
    userid = session["user_id"]
    useremail = session["user_email"]
    carrito_list = Ccarrito.listar_carrito(id_user=userid)
    user = Cusuario.obtener_usuario(correo_electronico = useremail)
    if carrito_list:
        carritoid = carrito_list[0]
    
    ## Capturamos la fecha 
    now1 = dt.now()
    fecha = now1.strftime('%Y-%m-%d %H:%M:%S')
    if request.method == "POST":
        ## DATOS DE TARJETA
        metodo = request.form["metodo"]
        tarjeta = request.form["tarjeta"]
        expiracion = request.form["expiracion"]
        cvv = request.form["cvv"]
        estado = "pagado"
        if metodo=="tarjeta" and not(tarjeta and expiracion and cvv):
            message = 'Verifica los datos de tu tarjeta'
            return render_template('users/registerPedido.html', message=message)
        else:
            estado = "pago pendiente"
            tarjeta = 0
        
        ##DATOS DE ENVIO
        provincia = request.form["provincia"]
        distrito = request.form["distrito"]
        direccion = request.form["direccion"]
        dir_envio = provincia+" / "+distrito+" / "+direccion
        if not(provincia and distrito and direccion):
            message = 'Verifica tus datos de envío'
            return render_template('users/registerPedido.html', message=message)
        
        ## DATOS DE COMPROBANTE
        comprobante = request.form["comprobante"]
        ruc = 0
        if request.form["ruc"]:
            ruc = int(request.form["ruc"])

        if not(comprobante=="factura" and len(str(ruc))==11):
            message = 'Verifica tu número RUC'
            return render_template('users/registerPedido.html', message=message)
    
        repartidor = "Motorizado 1"
        tarifa = 10
        if distrito!="Lima":
            tarifa = 15

        Pedid = Pedido(
            estado=estado,
            repartidor=repartidor,
            tipo_comprobante=comprobante,
            metodo_pago=metodo,
            direccion_envio=dir_envio,
            area_reparto=distrito,
            tarifa_envio=tarifa + int(carrito_list[2]),
            fecha_emision=fecha,
            fecha_entrega=fecha
        )

        result = Pedid.generar(id_user=userid, id_cart=carritoid)
        datos_list =[
            estado,                 ## Estado de la compra
            comprobante,            ## Tipo de comprobante
            user.primer_nombre,     ## Primer nombre del cliente
            user.primer_apellido,   ## Primer apellido
            user.segundo_apellido,  ## Segundo apellido
            dir_envio,              ## Direccion de envio de compras
            ruc,                    ## RUC del cliente(si lo hubiera)
            carrito_list[3],        ## Cantidad de productos comprados 
            carrito_list[2],        ## Monto del carrito
            tarifa,                 ## Tarifa de envío
            fecha                   ## Fecha que se realizó la compra
            ]
        if result:
            Ccarrito.cambiar_estado_carrito(id_user= carritoid)
            message = 'Se ha completado tu compra'
            return render_template('users/comprobante.html', message=message, datos_list=datos_list)
        else:
            error = 'No se ha podido pocesar tu compra'
            return render_template('users/registerPedido.html', product = carrito_list, error=error)
    return render_template('users/registerPedido.html', product = carrito_list)

#Ruta para listar todos los Carritos de compra
@app.route('/pedidogistorial')
def listar_pedido():
    userid = session["user_id"]
    compra_list = Cpedido.listarpedido(idprod=userid)
    return render_template("users/comprobante_list.html", compra_list=compra_list)

@app.route('/cancelarpedido/<id_ped>')
def cancelar_pedido(id_ped:int):
    cancelar = Cpedido.cancelarpedido(id_ped=id_ped)
    if cancelar:
        message = "Compra cancelada"
        return render_template("users/comprobante_list.html", message=message)
    else:
        message = "Ha ocurrido un erro al cancelar la compra"
    return render_template("users/comprobante_list.html", message=message)


if __name__ == "__main__":
    app.secret_key = "clave_super_ultra_secreta"

    app.run(port=3008,debug=True)
