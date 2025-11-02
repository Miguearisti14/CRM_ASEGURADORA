from django.http import JsonResponse
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from CRM.models import Usuarios
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Usuarios, Tipo_DNI, Roles, Empresa, Clientes, Ciudades, Productos, Canal_venta, Tipo_Poliza, Polizas, Departamentos, Reclamaciones
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def plans(request):
    return render(request, 'plans.html')

def obtener_ciudades(request, departamento_id):
    ciudades = Ciudades.objects.filter(id_departamento_id=departamento_id).values("id", "descripcion")
    return JsonResponse(list(ciudades), safe=False)

def consultar_clientes(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para acceder a esta sección.")
        return redirect("/login")

    try:
        asesor = Usuarios.objects.get(user=request.user)
    except Usuarios.DoesNotExist:
        messages.error(request, "Tu cuenta no está asociada a un perfil válido.")
        return redirect("/")

    clientes = Clientes.objects.filter(asesor=asesor)
    query = request.GET.get("q")
    producto_id = request.GET.get("producto")

    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) | Q(dni__icontains=query)
        )

    polizas = Polizas.objects.filter(dni_cliente__in=clientes).select_related("id_producto", "id_canal_venta")

    if producto_id:
        polizas = polizas.filter(id_producto_id=producto_id)

    datos_clientes = []
    for cliente in clientes:
        poliza = polizas.filter(dni_cliente=cliente).order_by("-fecha_inicio").first()
        datos_clientes.append({"cliente": cliente, "poliza": poliza})

    return render(request, "consultar.html", {
        "datos_clientes": datos_clientes,
        "query": query or "",
        "productos": Productos.objects.all()
    })



def detalle_cliente(request, dni):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión.")
        return redirect("/login")

    # Recuperar el asesor y su empresa
    try:
        asesor = Usuarios.objects.get(user=request.user)
    except Usuarios.DoesNotExist:
        messages.error(request, "Tu perfil no está asociado correctamente.")
        return redirect("/")

    # Buscar el cliente dentro de la misma empresa del asesor
    cliente = get_object_or_404(Clientes, dni=dni, asesor__empresa=asesor.empresa)
    poliza = Polizas.objects.filter(dni_cliente=cliente).order_by("-fecha_inicio").first()
    tipos_dni = Tipo_DNI.objects.all()
    departamentos = Departamentos.objects.all()
    ciudades = Ciudades.objects.filter(id_departamento=cliente.id_ciudad.id_departamento)

    # === ACTUALIZACIÓN DE DATOS ===
    if request.method == "POST":
        cliente.celular = request.POST.get("telefono")
        cliente.telefono = request.POST.get("telefono")
        cliente.correo = request.POST.get("correo")
        cliente.direccion = request.POST.get("direccion")

        tipo_dni_id = request.POST.get("tipo_dni")
        ciudad_id = request.POST.get("ciudad")

        if tipo_dni_id:
            cliente.id_tipo_dni_id = tipo_dni_id
        if ciudad_id:
            cliente.id_ciudad_id = ciudad_id

        cliente.save()
        messages.success(request, f"Cliente '{cliente.nombre}' actualizado correctamente.")
        return redirect("detalle_cliente", dni=dni)

    context = {
        "cliente": cliente,
        "poliza": poliza,
        "tipos_dni": tipos_dni,
        "departamentos": departamentos,
        "ciudades": ciudades,
    }
    return render(request, "cliente_detalle.html", context)


def detalle_poliza(request, dni):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión.")
        return redirect("/login")

    # Recuperar el asesor y su empresa
    try:
        asesor = Usuarios.objects.get(user=request.user)
    except Usuarios.DoesNotExist:
        messages.error(request, "Tu perfil no está asociado correctamente.")
        return redirect("/")

    # Buscar el cliente dentro de la misma empresa del asesor
    cliente = get_object_or_404(Clientes, dni=dni, asesor__empresa=asesor.empresa)
    poliza = Polizas.objects.filter(dni_cliente=cliente).order_by("-fecha_inicio").first()

    context = {
        "cliente": cliente,
        "poliza": poliza
    }
    return render(request, "poliza_detalle.html", context)


def eliminar_cliente(request, dni):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión.")
        return redirect("/login")

    asesor = get_object_or_404(Usuarios, user=request.user)
    cliente = get_object_or_404(Clientes, dni=dni, asesor__empresa=asesor.empresa)

    if request.method == "POST":
        cliente.delete()
        messages.success(request, "El cliente ha sido eliminado correctamente.")
        return redirect("consultar_clientes")

    messages.error(request, "Operación no permitida.")
    return redirect("detalle_cliente", dni=dni)



def resumen(request):
    # Validar autenticación
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para acceder al panel.")
        return redirect("/login")

    # Obtener el perfil del usuario
    try:
        usuario = Usuarios.objects.select_related("empresa").get(user=request.user)
        empresa = usuario.empresa
    except Usuarios.DoesNotExist:
        messages.error(request, "Tu cuenta no está asociada a una empresa.")
        return redirect("/login")

    # Obtener datos reales asociados a la empresa
    clientes_count = Clientes.objects.filter(asesor__empresa=empresa).count()
    reclamos_pendientes = Reclamaciones.objects.filter(
        dni_asesor__empresa=empresa,
        id_estado__descripcion__icontains="pendiente"
    ).count()
    polizas_vigentes = Polizas.objects.filter(
    dni_cliente__asesor__empresa=empresa
    ).count()

    # Opcional: puedes calcular ingresos o métricas adicionales si tienes campos monetarios
    ingresos_mes = 12450  # placeholder — lo puedes reemplazar con un cálculo real

    # Actividad reciente simulada (luego puedes reemplazar con una tabla de logs)
    actividad_reciente = [
        {"fecha": "2025-10-17", "usuario": "Ana López", "accion": "Ingreso de cliente", "detalle": "Carlos Pérez"},
        {"fecha": "2025-10-17", "usuario": "Juan Gómez", "accion": "Actualización de póliza", "detalle": "ID #4587"},
        {"fecha": "2025-10-16", "usuario": "Laura Ruiz", "accion": "Reclamo cerrado", "detalle": "Seguros Alfa"},
    ]

    context = {
        "empresa": empresa,
        "clientes_count": clientes_count,
        "reclamos_pendientes": reclamos_pendientes,
        "polizas_vigentes": polizas_vigentes,
        "ingresos_mes": ingresos_mes,
        "actividad_reciente": actividad_reciente
    }

    return render(request, "resumen.html", context)

def nuevoCliente(request):
    # Asegurar autenticación
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para registrar un cliente.")
        return redirect("/login")

    # Datos para los selects
    tipos_dni = Tipo_DNI.objects.all()
    productos = Productos.objects.all()
    canales = Canal_venta.objects.all()
    departamentos = Departamentos.objects.all()
    ciudades = Ciudades.objects.all()

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        dni = request.POST.get("dni")
        tipo_dni_id = request.POST.get("tipo_dni")
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")
        direccion = request.POST.get("direccion")
        producto_id = request.POST.get("producto")
        tipo_poliza_nombre = request.POST.get("poliza")
        canal_id = request.POST.get("canal")
        notas = request.POST.get("notas")
        ciudad_id = request.POST.get("ciudad")
        departamento_id = request.POST.get("departamento")

        # Recuperar asesor logueado
        try:
            asesor = Usuarios.objects.get(user=request.user)
        except Usuarios.DoesNotExist:
            messages.error(request, "Tu cuenta no está asociada a un perfil válido.")
            return redirect("/")

        # Validar duplicado
        if Clientes.objects.filter(dni=dni).exists():
            messages.warning(request, "Ya existe un cliente registrado con este DNI.")
            return redirect("/client_form/")

        # Crear cliente
        cliente = Clientes.objects.create(
            dni=dni,
            id_tipo_dni_id=tipo_dni_id,
            nombre=nombre,
            direccion=direccion or "",
            telefono=telefono or "",
            correo=correo or "",
            celular=telefono or "",
            id_ciudad_id=ciudad_id,
            asesor=asesor
        )

        # Calcular fecha de finalización según tipo de póliza
        fecha_inicio = date.today()

        tipo = tipo_poliza_nombre.lower()
        if tipo == "mensual":
            fecha_fin = fecha_inicio + timedelta(days=30)
        elif tipo == "trimestral":
            fecha_fin = fecha_inicio + timedelta(days=90)
        elif tipo == "semestral":
            fecha_fin = fecha_inicio + timedelta(days=180)
        else:  # anual u otro
            fecha_fin = fecha_inicio + timedelta(days=365)

        # Obtener o crear el tipo de póliza
        tipo_poliza, _ = Tipo_Poliza.objects.get_or_create(descripcion=tipo_poliza_nombre)

        # Crear la póliza asociada al cliente y a la empresa del asesor
        Polizas.objects.create(
            id_producto_id=producto_id,
            id_canal_venta_id=canal_id,
            dni_cliente=cliente,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        messages.success(request, f"Cliente '{cliente.nombre}' y su póliza se registraron correctamente.")
        return redirect("/resumen")

    # Render de la vista con todos los datos
    return render(request, 'client_form.html', {
        "productos": productos,
        "tipos_dni": tipos_dni,
        "canales": canales,
        "departamentos": departamentos,
        "ciudades": ciudades
    })

def interacciones(request):
    return render(request, 'interacciones.html')

def reclamaciones(request):
    return render(request, 'reclamaciones.html')

def reportes(request):
    return render(request, 'reportes.html')

# Autenticación e inicio de sesión
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Autenticación con el sistema de usuarios de Django
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Iniciar sesión
            login(request, user)

            try:
                # Buscar perfil extendido del usuario (modelo Usuarios)
                perfil = Usuarios.objects.select_related("id_rol", "empresa").get(user=user)
                rol = perfil.id_rol.nombre
                empresa = perfil.empresa
            except Usuarios.DoesNotExist:
                rol = "Sin rol asignado"
                empresa = None

            # Guardar información útil en la sesión
            request.session["rol"] = rol
            if empresa:
                request.session["empresa_id"] = empresa.id
                request.session["empresa_nombre"] = empresa.nombre
            else:
                request.session["empresa_id"] = None
                request.session["empresa_nombre"] = "Sin empresa"

            messages.success(request, f"Bienvenido {user.first_name}! Empresa: {request.session['empresa_nombre']}")

            return redirect("/resumen")
        else:
            messages.error(request, "Credenciales inválidas. Por favor, intenta nuevamente.")
            return redirect("/login")

    return render(request, "login.html")

# Cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('login')

# Registro de nuevas empresas
def register(request):
    tipos_dni = Tipo_DNI.objects.all()

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        dni = request.POST.get("dni")
        tipo_dni_id = request.POST.get("tipo_dni")
        celular = request.POST.get("celular")
        empresa_nombre = request.POST.get("empresa")

        # Validaciones
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("/register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Este correo ya está registrado.")
            return redirect("/register")

        if Empresa.objects.filter(nombre=empresa_nombre).exists():
            messages.error(request, "Ya existe una empresa registrada con ese nombre.")
            return redirect("/register")
        
        # Crear usuario base de Django
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

         # --- Asignar un rol por defecto ---
        rol_default = Roles.objects.filter(nombre__icontains="admin").first()
        if not rol_default:
            rol_default = Roles.objects.create(nombre="Administrador")

        # --- Crear empresa ---
        empresa = Empresa.objects.create(nombre=empresa_nombre)

        # --- Crear registro extendido ---
        usuario = Usuarios.objects.create(
            user=user,
            dni=dni,
            tipo_dni_id=tipo_dni_id,
            celular=celular,
            id_rol=rol_default,
            empresa=empresa 
        )

        # --- Actualizar empresa con su administrador ---
        empresa.usuario_admin = usuario
        empresa.save()

        messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect("/login")

    return render(request, "register.html", {"tipos_dni": tipos_dni})


def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("/login")







# Vista para crear un usuario administrador desde una interfaz web
def crear_admin_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validaciones
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("crear_admin")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese nombre de usuario ya existe.")
            return redirect("crear_admin")

        # Crear superusuario
        user = User.objects.create_superuser(username=username, email=email, password=password)
        messages.success(request, f"Usuario administrador '{username}' creado con éxito. Puedes iniciar sesión en /admin")

        return 
    return render(request, "crear_admin.html")
