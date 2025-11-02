from django.db import models
from django.contrib.auth.models import User


# ==============================
# TABLA DE ROLES
# ==============================
class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "roles"

# ==============================
# TABLA DE EMPRESAS
# ==============================
class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    usuario_admin = models.OneToOneField(
        "Usuarios", on_delete=models.SET_NULL, null=True, blank=True, related_name="empresa_admin"
    )
    
    class Meta:
        db_table = "empresas"

# ==============================
# TABLA DE TIPO DE DNI
# ==============================
class Tipo_DNI(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "Tipo_DNI"

# ==============================
# TABLA DE TIPO DE INTERACCIÓN
# ==============================
class TipoInteraccion(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "tipo_interaccion"

# ==============================
# TABLA DE ESTADOS DE RECLAMACIONES
# ==============================
class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "estados"

# ==============================
# TABLA DE RAMOS
# ==============================
class Ramos(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "ramos"


# ==============================
# TABLA DE TIPO DE POLIZA
# ==============================
class Tipo_Poliza(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, unique=True)
    valor = models.IntegerField(unique=True)

    class Meta:
        db_table = "tipo_poliza"

# ==============================
# TABLA DE CANALES DE VENTA
# ==============================
class Canal_venta(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "canal_venta"

# ==============================
# TABLA DE FORMAS DE PAGO
# ==============================
class Formas_pago(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "formas_pago"

# ==============================
# TABLA DE DEPARTAMENTOS
# ==============================
class Departamentos(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "departamentos"

# ==============================
# TABLA DE CIUDADES
# ==============================
class Ciudades(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, unique=True)
    id_departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE)

    class Meta:
        db_table = "ciudades"

# ==============================
# TABLA DE PRODUCTOS
# ==============================
class Productos(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, unique=True)
    id_ramo = models.ForeignKey(Ramos, on_delete=models.CASCADE)

    class Meta:
        db_table = "productos"

# ==============================
# TABLA DE CLIENTES
# ==============================
class Clientes(models.Model):
    dni = models.CharField(max_length=50, primary_key=True)
    id_tipo_dni = models.ForeignKey(Tipo_DNI, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    id_ciudad = models.ForeignKey(Ciudades, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    celular = models.CharField(max_length=50)
    correo = models.EmailField(blank=True, null=True)
    asesor = models.ForeignKey("Usuarios", on_delete=models.SET_NULL, null=True, blank=True, related_name="clientes")
    
    class Meta:
        db_table = "clientes"

# ==============================
# TABLA DE USUARIOS
# ==============================
class Usuarios(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=50, primary_key=True)
    tipo_dni = models.ForeignKey(Tipo_DNI, on_delete=models.CASCADE)
    celular = models.CharField(max_length=50)
    id_rol = models.ForeignKey(Roles, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True, related_name="usuarios")

    class Meta:
        db_table = "usuarios"

# ==============================
# TABLA DE INTERACCIONES
# ==============================
class Interacciones(models.Model):
    id = models.AutoField(primary_key=True)
    dni_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    dni_asesor = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    id_tipo_interaccion = models.ForeignKey(TipoInteraccion, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = "interacciones"

# ==============================
# TABLA DE PÓLIZAS
# ==============================
class Polizas(models.Model):
    id = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    id_canal_venta = models.ForeignKey(Canal_venta, on_delete=models.CASCADE)
    id_tipo_poliza = models.ForeignKey(Tipo_Poliza, on_delete=models.CASCADE)
    id_forma_pago = models.ForeignKey(Formas_pago, on_delete=models.CASCADE)
    dni_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = "polizas"

# ==============================
# TABLA DE RECLAMACIONES
# ==============================
class Reclamaciones(models.Model):
    id = models.AutoField(primary_key=True)
    dni_asesor = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    dni_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    poliza = models.ForeignKey(Polizas, on_delete=models.SET_NULL, null=True, db_column="id_poliza")
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)
    id_estado = models.ForeignKey(Estado, on_delete=models.CASCADE, db_column="id_estado", related_name="reclamacion_estado")

    class Meta:
        db_table = "reclamaciones"
