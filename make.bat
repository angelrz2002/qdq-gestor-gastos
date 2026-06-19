@echo off
if "%1"=="up" (
    echo [make] Levantando el ecosistema de gastos...
    
    :: Terminar procesos previos
    for /f "usebackq tokens=2 delims=," %%a in (`wmic process where "commandline like '%%uvicorn%%'" get ProcessId /format:csv 2^>nul`) do (
        if not "%%a"=="" if not "%%a"=="ProcessId" taskkill /F /T /PID %%a 2>nul
    )
    for /f "usebackq tokens=2 delims=," %%a in (`wmic process where "commandline like '%%vite%%'" get ProcessId /format:csv 2^>nul`) do (
        if not "%%a"=="" if not "%%a"=="ProcessId" taskkill /F /T /PID %%a 2>nul
    )
    for /f "usebackq tokens=2 delims=," %%a in (`wmic process where "commandline like '%%npm%%'" get ProcessId /format:csv 2^>nul`) do (
        if not "%%a"=="" if not "%%a"=="ProcessId" taskkill /F /T /PID %%a 2>nul
    )
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a 2>nul
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING') do taskkill /F /PID %%a 2>nul
    
    ping -n 2 127.0.0.1 >nul
    start "Backend - Gastos" cmd /c "cd /d backend-gastos && python -m uvicorn main:app --reload --port 8000"
    cd frontend-gastos && npm run dev
)
if "%1"=="down" (
    echo [make] Deteniendo servicios...
    
    for /f "usebackq tokens=2 delims=," %%a in (`wmic process where "commandline like '%%uvicorn%%'" get ProcessId /format:csv 2^>nul`) do (
        if not "%%a"=="" if not "%%a"=="ProcessId" taskkill /F /T /PID %%a 2>nul
    )
    for /f "usebackq tokens=2 delims=," %%a in (`wmic process where "commandline like '%%vite%%'" get ProcessId /format:csv 2^>nul`) do (
        if not "%%a"=="" if not "%%a"=="ProcessId" taskkill /F /T /PID %%a 2>nul
    )
    for /f "usebackq tokens=2 delims=," %%a in (`wmic process where "commandline like '%%npm%%'" get ProcessId /format:csv 2^>nul`) do (
        if not "%%a"=="" if not "%%a"=="ProcessId" taskkill /F /T /PID %%a 2>nul
    )
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a 2>nul
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING') do taskkill /F /PID %%a 2>nul
    
    echo [make] Todos los servicios detenidos.
)
if "%1"=="test" (
    if not exist "%~dp0backend-gastos\doc" mkdir "%~dp0backend-gastos\doc"
    echo # Reporte de Pruebas Unitarias Autogenerado
    echo Fecha de ejecucion: %DATE% %TIME%
    echo ```text
    
    echo # Reporte de Pruebas Unitarias Autogenerado > "%~dp0backend-gastos\doc\test_results.md"
    echo Fecha de ejecucion: %DATE% %TIME% >> "%~dp0backend-gastos\doc\test_results.md"
    echo ```text >> "%~dp0backend-gastos\doc\test_results.md"
    
    cd /d "%~dp0backend-gastos"
    python -m pytest --verbose
    python -m pytest --verbose >> "%~dp0backend-gastos\doc\test_results.md" 2>&1
    cd /d "%~dp0"
    
    echo ```
    echo ``` >> "%~dp0backend-gastos\doc\test_results.md"
)
