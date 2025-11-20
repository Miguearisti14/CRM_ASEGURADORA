import os
import sys
import shutil
import subprocess
import tempfile
import threading
import time
import webbrowser
import sqlite3

PROJECT_DIR_NAME = "CRM_Aseguradoras"
APP_URL = "http://127.0.0.1:8000"

def get_base_path():
    """Obtiene la ruta base (funciona en .exe y script)."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def setup_project():
    """Configura el proyecto en una ubicación permanente."""
    # Carpeta de datos del usuario
    app_data = os.path.join(os.environ['APPDATA'], 'ZuluArisCRM')
    os.makedirs(app_data, exist_ok=True)
    
    project_path = os.path.join(app_data, PROJECT_DIR_NAME)
    
    # Si no existe, copiar desde el ejecutable
    if not os.path.exists(project_path):
        base_path = get_base_path()
        source_project = os.path.join(base_path, PROJECT_DIR_NAME)
        
        print("📦 Instalando aplicación por primera vez...")
        shutil.copytree(
            source_project,
            project_path,
            ignore=shutil.ignore_patterns("*.pyc", "__pycache__", "*.log")
        )
        
        # Copiar base de datos incluida
        db_source = os.path.join(source_project, 'db.sqlite3')
        if os.path.exists(db_source):
            shutil.copy2(db_source, os.path.join(project_path, 'db.sqlite3'))
    
    return project_path

def run_django(project_path):
    """Ejecuta el servidor Django."""
    manage_py = os.path.join(project_path, "manage.py")
    
    # Asegurar que Python encuentre el proyecto
    sys.path.insert(0, project_path)
    
    cmd = [sys.executable, manage_py, "runserver", "127.0.0.1:8000", "--noreload"]
    
    subprocess.call(cmd, cwd=project_path)

def open_app_window():
    """Abre el navegador en modo app."""
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    edge_paths = [
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    ]

    for path in chrome_paths:
        if os.path.exists(path):
            subprocess.Popen([path, f'--app={APP_URL}'])
            return

    for path in edge_paths:
        if os.path.exists(path):
            subprocess.Popen([path, f'--app={APP_URL}'])
            return

    webbrowser.open(APP_URL)

def main():
    print("🚀 Iniciando ZuluAris CRM...")
    
    project_path = setup_project()
    
    print("⚙️  Iniciando servidor...")
    django_thread = threading.Thread(target=run_django, args=(project_path,))
    django_thread.daemon = True
    django_thread.start()

    print("⏳ Esperando al servidor...")
    time.sleep(5)

    print("🌐 Abriendo aplicación...")
    open_app_window()

    try:
        print("\n✅ Aplicación ejecutándose en:", APP_URL)
        print("❌ Presiona Ctrl+C para cerrar")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🔴 Cerrando servidor...")
        sys.exit(0)

if __name__ == "__main__":
    main()
