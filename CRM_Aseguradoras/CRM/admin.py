from django.contrib import admin
from .models import (
    Roles, Tipo_DNI, TipoInteraccion, Estado, Ramos,
    Tipo_Poliza, Canal_venta, Formas_pago, Departamentos,
    Ciudades, Productos, Clientes, Usuarios, Interacciones,
    Polizas, Reclamaciones
)

admin.site.register(Roles)
admin.site.register(Tipo_DNI)
admin.site.register(TipoInteraccion)
admin.site.register(Estado)
admin.site.register(Ramos)
admin.site.register(Tipo_Poliza)
admin.site.register(Canal_venta)
admin.site.register(Formas_pago)
admin.site.register(Departamentos)
admin.site.register(Ciudades)
admin.site.register(Productos)
admin.site.register(Clientes)
admin.site.register(Usuarios)
admin.site.register(Interacciones)
admin.site.register(Polizas)
admin.site.register(Reclamaciones)