@echo off
title Instalador ZuluAris CRM
color 0A

echo ========================================
echo   INSTALADOR ZULUARIS CRM v1.0
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no instalado.
    echo Descarga Python desde: https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH"
    pause
    exit /b 1
)

echo [OK] Python detectado

REM Instalar dependencias
echo.
echo Instalando dependencias necesarias...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Fallo al instalar dependencias
    pause
    exit /b 1
)

echo.
echo [OK] Dependencias instaladas

REM Aplicar migraciones (por si acaso)
echo.
echo Verificando base de datos...
python manage.py migrate --noinput

echo.
echo ========================================
echo   INSTALACION COMPLETADA
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo    1. Doble clic en "ejecutar.bat"
echo    2. Se abrira automaticamente en tu navegador
echo.
pause