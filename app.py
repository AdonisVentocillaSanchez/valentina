from functools import wraps
from flask import Flask, render_template, request, redirect, session
from models.usuario import Usuario
from models.producto import Producto
from models.comercio import Comercio
from models.pedido import Pedido
from models.carrito import Carrito
from models.categoria import Categoria

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
 
#Ruta para logueo de usuarios
@app.route('/inicio-sesion', methods=["get","post"])
def login():
    if request.method == "POST":
        correo_electronico=request.form["email"]
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

        if request.form["password"] == comercio.contrasena:

            session['user_name'] = comercio.RUC
            session['type'] = 2
            return redirect("/")
        else:
            error = 'Invalid password'
            return render_template('users/loginComercio.html', error=error)

    return render_template('users/loginComercio.html')

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
            return redirect("/")
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
    product_list = Cproducto.buscar_productos_categoria(idCategoria)

    if request.method == "POST":
        nombre = request.form["search"]

        product = Cproducto.buscar_producto_categoria(nombre, idCategoria)

        if not product:
            return render_template("users/products_list.html",product_list=product, error = "Producto no encontrado")
        else:
            return render_template("users/products_list.html",product_list=product)

    return render_template("users/products_list.html",product_list=product_list)

#Ruta para añadir al carrito un producto
@app.route('/addcarrito/<id_producto>')
def add_cart(id_producto):
    idProducto = int(id_producto)
    product = Cproducto.buscar_producto(idProducto)
    id_user = session["user_id"]
    precio_prod = product[5]
    stock = product[7]
    
    if stock>0:
        Ccarrito.agregar(cod_usu=id_user, precio=precio_prod)
        Cproducto.actualizar_producto_stock(id_prod=idProducto)
        return render_template("users/products_list.html",message = "Producto añadido al carrito")
    else:
        return render_template("users/products_list.html",message = "Disculpa, este producto está sin stock")
    
    return render_template("users/products_list.html",error = precio_prod)
    

#Ruta para listar un el carrito de compras
@app.route('/carrito')
@login_required
def view_cart():
    idUser = session["user_id"]
    carrito = Ccarrito.listar_carrito(id_user=idUser)

    return render_template("users/carrito_detail.html", product=carrito)

#Ruta para realizar un pedido a partir del carrito de compras
@app.route('/pedido', methods=["get","post"])
@login_required
def registrarPedido():

    if request.method == "POST":
        provincia = request.form["provincia"]
        direccion = request.form["direccion"]
        distrito = request.form["distrito"]
        ruc = int(request.form["ruc"])
        comprobante = request.form["comprobante"]
        tarjeta = request.form["tarjeta"]
        expiracion = request.form["direccion"]
        cvv = request.form["cvv"]

        

        if 1:
            return redirect("/")
        else:
            error = 'No se ha podido pocesar tu compra'
            return render_template('users/registerPedido.html', error=error)

    return render_template('users/registerProduct.html')

if __name__ == "__main__":
    app.secret_key = "clave_super_ultra_secreta"

    app.run(port=3008,debug=True)
