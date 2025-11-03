from django.http import JsonResponse
from datetime import date, timedelta, timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from CRM.models import Usuarios
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Interacciones, TipoInteraccion, Usuarios,Formas_pago, Tipo_Poliza, Canal_venta, Tipo_DNI, Roles, Empresa, Clientes, Ciudades, Productos, Canal_venta, Tipo_Poliza, Polizas, Departamentos, Reclamaciones
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def plans(request):
    return render(request, 'plans.html')

def obtener_ciudades(request, departamento_id):
    ciudades = Ciudades.objects.filter(id_departamento_id=departamento_id).values("id", "descripcion")
    return JsonResponse(list(ciudades), safe=False)


#----------------------------#
#-----CLIENTES Y POLIZAS-----#
#----------------------------#

# Vista y lógica para mostrar y gestionar clientes y sus pólizas
def gestionar_clientes(request):
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

    # Obtener todas las pólizas para los clientes filtrados
    polizas = Polizas.objects.filter(dni_cliente__in=clientes).select_related("id_producto", "id_canal_venta")

    if producto_id:
        polizas = polizas.filter(id_producto_id=producto_id)

    # Crear una estructura que contenga cada cliente con todas sus pólizas
    datos_clientes = []
    for cliente in clientes:
        polizas_cliente = polizas.filter(dni_cliente=cliente).order_by("-fecha_inicio")
        datos_clientes.append({
            "cliente": cliente,
            "polizas": polizas_cliente
        })

    return render(request, "consultar.html", {
        "datos_clientes": datos_clientes,
        "query": query or "",
        "productos": Productos.objects.all()
    })


# Mostrar en detalle la información de un cliente específico
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


# Mostrar en detalle la información de una póliza específica
def detalle_poliza(request, poliza_id):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión.")
        return redirect("/login")

    # Recuperar el asesor y su empresa
    try:
        asesor = Usuarios.objects.get(user=request.user)
    except Usuarios.DoesNotExist:
        messages.error(request, "Tu perfil no está asociado correctamente.")
        return redirect("/")

    # Buscar la póliza específica
    poliza = get_object_or_404(
        Polizas, 
        id=poliza_id, 
        dni_cliente__asesor__empresa=asesor.empresa
    )
    cliente = poliza.dni_cliente

    context = {
        "cliente": cliente,
        "poliza": poliza
    }
    return render(request, "poliza_detalle.html", context)

# Eliminar una póliza específica
def eliminar_poliza(request, poliza_id):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión.")
        return redirect("/login")

    try:
        asesor = Usuarios.objects.get(user=request.user)
    except Usuarios.DoesNotExist:
        messages.error(request, "Tu cuenta no está asociada correctamente.")
        return redirect("/")

    poliza = get_object_or_404(Polizas, id=poliza_id, dni_cliente__asesor__empresa=asesor.empresa)

    if request.method == "POST":
        poliza.delete()
        messages.success(request, "La póliza ha sido eliminada correctamente.")
        return redirect("gestionar_clientes")

    messages.warning(request, "Operación no permitida.")
    return redirect("detalle_poliza", dni=poliza.dni_cliente.dni)

# Renovar una póliza específica
def renovar_poliza(request, poliza_id):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión.")
        return redirect("/login")

    asesor = get_object_or_404(Usuarios, user=request.user)
    poliza = get_object_or_404(
        Polizas,
        id=poliza_id,
        dni_cliente__asesor__empresa=asesor.empresa
    )

    if request.method == "POST":
        tipo = poliza.id_tipo_poliza.valor
        fecha_fin_actual = poliza.fecha_fin

        # Lógica para extender la fecha según el tipo de póliza
        if tipo == 1:  # mensual
            poliza.fecha_fin = fecha_fin_actual + timedelta(days=30)
        elif tipo == 3:  # trimestral
            poliza.fecha_fin = fecha_fin_actual + timedelta(days=90)
        elif tipo == 6:  # semestral
            poliza.fecha_fin = fecha_fin_actual + timedelta(days=180)
        elif tipo == 12:  # anual
            poliza.fecha_fin = fecha_fin_actual + timedelta(days=365)
        else:
            messages.warning(request, "No se pudo determinar la duración del tipo de póliza.")
            return redirect("detalle_poliza", dni=poliza.dni_cliente.dni)

        poliza.save()
        messages.success(request, f"La póliza #{poliza.id} fue renovada correctamente.")
        return redirect("detalle_poliza", poliza_id=poliza.id)

    messages.error(request, "Operación no permitida.")
    return redirect("detalle_poliza", poliza_id=poliza.id)

# Eliminar un cliente específico
def eliminar_cliente(request, dni):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión.")
        return redirect("/login")

    asesor = get_object_or_404(Usuarios, user=request.user)
    cliente = get_object_or_404(Clientes, dni=dni, asesor__empresa=asesor.empresa)

    if request.method == "POST":
        cliente.delete()
        messages.success(request, "El cliente ha sido eliminado correctamente.")
        return redirect("gestionar_clientes")

    messages.error(request, "Operación no permitida.")
    return redirect("detalle_cliente", dni=dni)

# Crear un nuevo cliente junto con su póliza inicial
def nuevoCliente(request):
    # Asegurar autenticación
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para registrar un cliente.")
        return redirect("/login")

    # Datos para los selects
    tipos_dni = Tipo_DNI.objects.all()
    tipo_polizas = Tipo_Poliza.objects.all()
    productos = Productos.objects.all()
    canales = Canal_venta.objects.all()
    departamentos = Departamentos.objects.all()
    ciudades = Ciudades.objects.all()
    metodos = Formas_pago.objects.all()

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        dni = request.POST.get("dni")
        tipo_dni_id = request.POST.get("tipo_dni")
        correo = request.POST.get("correo")
        telefono = request.POST.get("telefono")
        direccion = request.POST.get("direccion")
        producto_id = request.POST.get("producto")
        tipo_poliza_id = request.POST.get("poliza")
        canal_id = request.POST.get("canal")
        ciudad_id = request.POST.get("ciudad")
        departamento_id = request.POST.get("metodo")
        metodo_pago_id = request.POST.get("metodo")

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

        tipo =  get_object_or_404(Tipo_Poliza, id=tipo_poliza_id).valor
        if tipo == 1:  # mensual
            fecha_fin = fecha_inicio + timedelta(days=30)
        elif tipo == 3:  # trimestral"
            fecha_fin = fecha_inicio + timedelta(days=90)
        elif tipo == 6:  # semestral
            fecha_fin = fecha_inicio + timedelta(days=180)
        else:  # anual u otro
            fecha_fin = fecha_inicio + timedelta(days=365)


        # Crear la póliza asociada al cliente y a la empresa del asesor
        Polizas.objects.create(
            id_producto_id=producto_id,
            id_canal_venta_id=canal_id,
            dni_cliente=cliente,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            id_tipo_poliza_id=tipo_poliza_id,
            id_forma_pago_id=metodo_pago_id
        )

        messages.success(request, f"Cliente '{cliente.nombre}' y su póliza se registraron correctamente.")
        return redirect("/resumen")

    # Render de la vista con todos los datos
    return render(request, 'client_form.html', {
        "productos": productos,
        "tipos_dni": tipos_dni,
        "canales": canales,
        "departamentos": departamentos,
        "ciudades": ciudades,
        "tipos": tipo_polizas,
        "metodos": metodos
    })


# Crear poliza para usuario ya existente
def crear_poliza(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para registrar una póliza.")
        return redirect("/login")

    # Obtener el asesor logueado
    asesor = get_object_or_404(Usuarios, user=request.user)


    clientes = Clientes.objects.filter(asesor__empresa=asesor.empresa)


    # Cargar datos para los selects
    productos = Productos.objects.all()
    tipos_poliza = Tipo_Poliza.objects.all()
    canales = Canal_venta.objects.all()
    metodos = Formas_pago.objects.all()

    if request.method == "POST":
        dni_cliente_id = request.POST.get("cliente")
        producto_id = request.POST.get("producto")
        tipo_poliza_id = request.POST.get("tipo_poliza")
        canal_id = request.POST.get("canal")
        metodo_pago_id = request.POST.get("metodo")

        # Validación básica
        if not dni_cliente_id or not producto_id or not tipo_poliza_id:
            messages.error(request, "Por favor completa todos los campos obligatorios.")
            return redirect("crear_poliza")

        cliente = get_object_or_404(Clientes, dni=dni_cliente_id)

        fecha_inicio = date.today()

        tipo =  get_object_or_404(Tipo_Poliza, id=tipo_poliza_id).valor
        if tipo == 1:  # mensual
            fecha_fin = fecha_inicio + timedelta(days=30)
        elif tipo == 3:  # trimestral"
            fecha_fin = fecha_inicio + timedelta(days=90)
        elif tipo == 6:  # semestral
            fecha_fin = fecha_inicio + timedelta(days=180)
        else:  # anual u otro
            fecha_fin = fecha_inicio + timedelta(days=365)

        # Crear póliza
        Polizas.objects.create(
            id_producto_id=producto_id,
            id_canal_venta_id=canal_id,
            dni_cliente=cliente,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            id_tipo_poliza_id=tipo_poliza_id,
            id_forma_pago_id=metodo_pago_id
        )


        messages.success(request, f"La póliza para {cliente.nombre} se registró correctamente.")
        return redirect("gestionar_clientes")

    return render(request, "crear_poliza.html", {
        "titulo": "Registrar nueva póliza",
        "descripcion": "Asigna una nueva póliza a un cliente existente.",
        "clientes": clientes,
        "productos": productos,
        "tipos_poliza": tipos_poliza,
        "canales": canales,
        "metodos": metodos 
    })


#----------------------------#
#-----PANTALLA PRINCIPAL-----#
#----------------------------#
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



#----------------------------#
#------- INTERACCIONES ------#
#----------------------------#

# Vista para gestionar interacciones
def interacciones(request):
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para acceder a esta sección.")
        return redirect("/login")

    try:
        asesor = Usuarios.objects.get(user=request.user)
    except Usuarios.DoesNotExist:
        messages.error(request, "Tu cuenta no está asociada a un perfil válido.")
        return redirect("/")

    # Base: interacciones solo del asesor actual
    interacciones = Interacciones.objects.filter(dni_asesor=asesor).select_related(
        "dni_cliente", "id_tipo_interaccion"
    )

    # --- Filtros ---
    query = request.GET.get("q")  # nombre o dni del cliente
    tipo_id = request.GET.get("tipo")

    if query:
        interacciones = interacciones.filter(
            Q(dni_cliente__nombre__icontains=query)
            | Q(dni_cliente__dni__icontains=query)
            | Q(asunto__icontains=query)
        )

    if tipo_id:
        interacciones = interacciones.filter(id_tipo_interaccion_id=tipo_id)

    # Orden descendente (últimas primero)
    interacciones = interacciones.order_by("-fecha")


    context = {
        "interacciones": interacciones,
        "tipos": TipoInteraccion.objects.all(),
        "query": query or "",
        "tipo_id": tipo_id or "",
    }
    return render(request, "interacciones.html", context)

# Registrar una nueva interacción 
def registrar_interaccion(request):
    # ✅ Verificar autenticación
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para registrar una interacción.")
        return redirect("/login")

    # ✅ Obtener asesor logueado
    asesor = get_object_or_404(Usuarios, user=request.user)

    # ✅ Obtener clientes del asesor (solo de su empresa)
    clientes = Clientes.objects.filter(asesor__empresa=asesor.empresa)

    # ✅ Obtener tipos de interacción (llamada, correo, reunión, etc.)
    tipos_interaccion = TipoInteraccion.objects.all()

    # ✅ Si se envió el formulario
    if request.method == "POST":
        dni_cliente_id = request.POST.get("cliente")
        tipo_id = request.POST.get("tipo_interaccion")
        asunto = request.POST.get("asunto")
        observaciones = request.POST.get("observaciones")

        # ⚠️ Validación básica
        if not dni_cliente_id or not tipo_id or not asunto:
            messages.error(request, "Por favor completa todos los campos obligatorios.")
            return redirect("interaccion")

        # ✅ Buscar cliente
        cliente = get_object_or_404(Clientes, dni=dni_cliente_id)

        # ✅ Crear interacción
        Interacciones.objects.create(
            dni_cliente=cliente,
            dni_asesor=asesor,
            id_tipo_interaccion_id=tipo_id,
            asunto=asunto,
            observaciones=observaciones
        )

        messages.success(request, f"La interacción con {cliente.nombre} se registró correctamente.")
        return redirect("interacciones")

    # ✅ Renderizar formulario
    return render(request, "interaccion_form.html", {
        "titulo": "Registrar nueva interacción",
        "descripcion": "Registra una nueva interacción con un cliente de tu cartera.",
        "clientes": clientes,
        "tipos_interaccion": tipos_interaccion
    })



#----------------------------#
#------- RECLAMACIONES ------#
#----------------------------#

def reclamaciones(request):
    return render(request, 'reclamaciones.html')

#----------------------------#
#--------- REPORTES ---------#
#----------------------------#

def reportes(request):
    return render(request, 'reportes.html')


#----------------------------#
#------- LOGIN Y AUTH -------#
#----------------------------#
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

# Cierre de sesión
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
