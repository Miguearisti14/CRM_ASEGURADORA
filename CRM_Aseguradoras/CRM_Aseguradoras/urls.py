import CRM.views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CRM.views.index),
    path('register/', CRM.views.register),
    path('plans/', CRM.views.plans),
    path('gestionar/', CRM.views.gestionar_clientes, name='gestionar_clientes'),
    path('resumen/', CRM.views.resumen, name='panel_resumen'),
    path('client_form/', CRM.views.nuevoCliente),
    path('interacciones/', CRM.views.interacciones, name='interacciones'),
    path('reclamaciones/', CRM.views.reclamaciones),
    path('reportes/', CRM.views.reportes),
    path('login/', CRM.views.login_view),
    path('crear_admin/', CRM.views.crear_admin_view, name='crear_admin'),
    path("logout/", CRM.views.logout_view),
    path('clientes/<str:dni>/', CRM.views.detalle_cliente, name='detalle_cliente'),
    path('poliza/<int:poliza_id>/', CRM.views.detalle_poliza, name='detalle_poliza'),
    path('poliza/<int:poliza_id>/eliminar', CRM.views.eliminar_poliza, name='eliminar_poliza'),
    path('poliza/<int:poliza_id>/renovar', CRM.views.renovar_poliza, name='renovar_poliza'),
    path('clientes/<str:dni>/eliminar/', CRM.views.eliminar_cliente, name='eliminar_cliente'),
    path("ajax/ciudades/<int:departamento_id>/", CRM.views.obtener_ciudades, name="obtener_ciudades"),
    path('gestionar/crear/', CRM.views.crear_poliza, name='crear_poliza'),
    path('interacciones/registrar/', CRM.views.registrar_interaccion, name='registrar_interaccion'),
    path('interacciones/<int:interaccion_id>/', CRM.views.detalle_interaccion, name='detalle_interaccion'),
    path('reclamaciones/', CRM.views.reclamaciones, name='reclamaciones'),
    path('reclamaciones/crear/', CRM.views.crear_reclamacion, name='crear_reclamacion'),
    path("api/polizas-cliente/<str:dni>/", CRM.views.polizas_por_cliente, name="polizas_por_cliente"),
    path('polizas-cliente/<str:dni>/', CRM.views.polizas_por_cliente, name='polizas_por_cliente'),
    path('reclamaciones/<int:reclamacion_id>/', CRM.views.detalle_reclamacion, name='detalle_reclamacion'),
    path("reclamaciones/<int:reclamacion_id>/estado/", CRM.views.cambiar_estado_reclamacion, name="cambiar_estado_reclamacion"),
    path("reclamaciones/<int:reclamacion_id>/eliminar/", CRM.views.eliminar_reclamacion, name="eliminar_reclamacion"),

]
