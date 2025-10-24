from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from CRM.models import Usuarios
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Usuarios, Tipo_DNI, Roles

# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    tipos_dni = Tipo_DNI.objects.all()

    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        dni = request.POST["dni"]
        tipo_dni_id = request.POST["tipo_dni"]
        celular = request.POST["celular"]

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("register")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Este correo ya está registrado.")
            return redirect("register")

        # Crear usuario base de Django
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        # Asignar un rol por defecto (por ejemplo, Asesor)
        rol_default = Roles.objects.first()

        # Crear registro extendido
        Usuarios.objects.create(
            user=user,
            dni=dni,
            tipo_dni_id=tipo_dni_id,
            celular=celular,
            id_rol=rol_default
        )
        print("Tipos DNI:", tipos_dni)
        messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect("login.html")
    

    return render(request, "register.html", {"tipos_dni": tipos_dni})


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

        # Autenticación usando el sistema de auth nativo
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si las credenciales son correctas, iniciar sesión
            login(request, user)

            # Si el usuario tiene un registro en la tabla Usuarios, podemos acceder a su rol
            try:
                perfil = Usuarios.objects.get(user=user)
                rol = perfil.id_rol.nombre
            except Usuarios.DoesNotExist:
                rol = "Sin rol asignado"

            # Guardar el rol en la sesión si quieres usarlo en el panel
            request.session["rol"] = rol

            # Redirigir al panel principal del CRM
            return redirect("panel_resumen")
        else:
            # Error de autenticación
            return render(request, "login.html", {"error": "Credenciales inválidas"})

    return render(request, "login.html")


# Cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('login')

