@echo off
title ZuluAris CRM - Servidor Activo
color 0B

echo ========================================
echo   ZULUARIS CRM - INICIANDO...
echo ========================================
echo.

REM Esperar 3 segundos y abrir navegador
start /B cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:8000"

echo [*] Servidor ejecutandose en: http://127.0.0.1:8000
echo [*] Para detener: Cierra esta ventana
echo.
echo ========================================

REM Iniciar servidor Django
python manage.py runserver 127.0.0.1:8000

pause