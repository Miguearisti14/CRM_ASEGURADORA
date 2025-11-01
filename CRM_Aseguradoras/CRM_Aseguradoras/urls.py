import CRM.views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CRM.views.index),
    path('register/', CRM.views.register),
    path('plans/', CRM.views.plans),
    path('consultar/', CRM.views.consultar_clientes, name='consultar_clientes'),
    path('resumen/', CRM.views.resumen),
    path('client_form/', CRM.views.nuevoCliente),
    path('interacciones/', CRM.views.interacciones),
    path('reclamaciones/', CRM.views.reclamaciones),
    path('reportes/', CRM.views.reportes),
    path('login/', CRM.views.login_view),
    path('crear_admin/', CRM.views.crear_admin_view, name='crear_admin'),
    path("logout/", CRM.views.logout_view),
    path('clientes/<str:dni>/', CRM.views.detalle_cliente, name='detalle_cliente'),
    path('clientes/<str:dni>/eliminar/', CRM.views.eliminar_cliente, name='eliminar_cliente'),
    path("ajax/ciudades/<int:departamento_id>/", CRM.views.obtener_ciudades, name="obtener_ciudades"),


]
