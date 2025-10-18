from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

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