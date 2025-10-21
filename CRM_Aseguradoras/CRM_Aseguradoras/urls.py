import CRM.views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CRM.views.index),
    path('register/', CRM.views.register),
    path('plans/', CRM.views.plans),
    path('consultar/', CRM.views.consultar),
    path('resumen/', CRM.views.resumen),
    path('client_form/', CRM.views.nuevoCliente),
    path('interacciones/', CRM.views.interacciones),
    path('reclamaciones/', CRM.views.reclamaciones),
    path('reportes/', CRM.views.reportes),
]
