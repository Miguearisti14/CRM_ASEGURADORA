import CRM.views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("panel_admin/", CRM.views.panel_admin, name="admin_panel"),
    path('', CRM.views.index),
    path('register/', CRM.views.register),
    path('plans/', CRM.views.plans),
    path('gestionar/', CRM.views.gestionar_clientes, name='gestionar_clientes'),
    path('resumen/', CRM.views.resumen, name='panel_resumen'),
    path('client_form/', CRM.views.nuevoCliente),
    path('interacciones/', CRM.views.interacciones, name='interacciones'),
    path('reclamaciones/', CRM.views.reclamaciones),
    path('login/', CRM.views.login_view),
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
    path("reportes/", CRM.views.reportes_panel, name="reportes_panel"),
    path("reportes/exportar/<str:tipo>/", CRM.views.exportar_reporte, name="exportar_reporte"),
    path("reportes/metricas/", CRM.views.reportes_metricas, name="reportes_metricas"),
    path("usuarios/", CRM.views.gestionar_usuarios, name="gestionar_usuarios"),
    path("usuarios/crear/", CRM.views.crear_usuario, name="crear_usuario"),
    path("usuarios/<str:dni>/detalle/", CRM.views.detalle_usuario, name="detalle_usuario"),
    path("usuarios/<str:dni>/eliminar/", CRM.views.eliminar_usuario, name="eliminar_usuario"),

    path("datos/", CRM.views.gestionar_datos, name="gestionar_datos"),
    path("datos/crear/<str:recurso>/", CRM.views.crear_dato, name="crear_dato"),
    path("datos/eliminar/<str:recurso>/<int:pk>/", CRM.views.eliminar_dato, name="eliminar_dato"),

    path("reportes_admin/", CRM.views.reportes_admin, name="reportes_admin"),
    path("reportes/metricas_admin/", CRM.views.reportes_metricas_admin, name="reportes_metricas_admin"),

]
