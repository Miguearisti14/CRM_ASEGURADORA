from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from CRM.models import Usuarios
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Usuarios, Tipo_DNI, Roles, Empresa

# Create your views here.
def index(request):
    return render(request, 'index.html')




def plans(request):
    return render(request, 'plans.html')

def consultar(request):
    return render(request, 'consultar.html')

def resumen(request):
    return render(request, 'resumen.html')

def nuevoCliente(request):
    return render(request, 'client_form.html')

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

            # Mensaje de bienvenida opcional
            messages.success(request, f"Bienvenido {user.first_name}! Empresa: {request.session['empresa_nombre']}")

            # Redirigir al panel principal
            return redirect("panel_resumen")

        else:
            # Credenciales inválidas
            messages.error(request, "Credenciales inválidas. Por favor, intenta nuevamente.")
            return render(request, "login.html")

    # Renderizar el formulario en GET
    return render(request, "login.html")

# Cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('login')

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
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Este correo ya está registrado.")
            return redirect("register")

        if Empresa.objects.filter(nombre=empresa_nombre).exists():
            messages.error(request, "Ya existe una empresa registrada con ese nombre.")
            return redirect("register")

        # Crear usuario base de Django
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        # Asignar un rol por defecto (por ejemplo "Administrador")
        rol_default = Roles.objects.filter(nombre__icontains="admin").first()
        if not rol_default:
            rol_default = Roles.objects.create(nombre="Administrador")

        # Crear registro en tabla Usuarios
        usuario = Usuarios.objects.create(
            user=user,
            dni=dni,
            tipo_dni_id=tipo_dni_id,
            celular=celular,
            id_rol=rol_default,
            empresa = empresa_nombre
        )

        # Crear la empresa asociada
        empresa = Empresa.objects.create(
            nombre=empresa_nombre,
            usuario_admin=usuario
        )

        messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect("login")

    return render(request, "register.html", {"tipos_dni": tipos_dni})










def crear_admin_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validaciones básicas
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("crear_admin")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Ese nombre de usuario ya existe.")
            return redirect("crear_admin")

        # Crear superusuario
        user = User.objects.create_superuser(username=username, email=email, password=password)
        messages.success(request, f"Usuario administrador '{username}' creado con éxito. Puedes iniciar sesión en /admin")

        return redirect("login_admin")  # o al home, si prefieres

    return render(request, "crear_admin.html")
