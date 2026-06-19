# ============================================================================
# MAKEFILE DE DESARROLLO - PROYECTO GASTOS QDQ
# ============================================================================

.PHONY: up down test

# Variables de Desarrollo
BACKEND_DIR = backend-gastos
FRONTEND_DIR = frontend-gastos
BACKEND_PORT = 8000
FRONTEND_PORT = 5173

# Detectar sistema operativo y configurar herramientas
ifeq ($(OS),Windows_NT)
	PYTHON = python
	NPM = npm
	STOP_BACKEND = for /f "usebackq tokens=2 delims=," %%a in (`wmic process where "commandline like '%%uvicorn%%'" get ProcessId /format:csv 2^>nul`) do (if not "%%a"=="" if not "%%a"=="ProcessId" taskkill /F /T /PID %%a 2>nul) & for /f "tokens=5" %%a in ('netstat -ano ^| findstr :$(BACKEND_PORT) ^| findstr LISTENING') do taskkill /F /PID %%a 2>nul || echo Backend detenido
	STOP_FRONTEND = for /f "usebackq tokens=2 delims=," %%a in (`wmic process where "commandline like '%%vite%%'" get ProcessId /format:csv 2^>nul`) do (if not "%%a"=="" if not "%%a"=="ProcessId" taskkill /F /T /PID %%a 2>nul) & for /f "usebackq tokens=2 delims=," %%a in (`wmic process where "commandline like '%%npm%%'" get ProcessId /format:csv 2^>nul`) do (if not "%%a"=="" if not "%%a"=="ProcessId" taskkill /F /T /PID %%a 2>nul) & for /f "tokens=5" %%a in ('netstat -ano ^| findstr :$(FRONTEND_PORT) ^| findstr LISTENING') do taskkill /F /PID %%a 2>nul || echo Frontend detenido
	SLEEP = ping -n 2 127.0.0.1 >nul
	RUN_BACKEND = $(PYTHON) -m uvicorn main:app --reload --port $(BACKEND_PORT)
	RUN_TESTS = cmd /c "echo # Reporte de Pruebas Unitarias Autogenerado && echo Fecha de ejecución: %DATE% %TIME% && echo ^`^`^`text && python -m pytest --verbose && echo ^`^`^` && echo # Reporte de Pruebas Unitarias Autogenerado> doc\test_results.md && echo Fecha de ejecución: %DATE% %TIME%>> doc\test_results.md && echo ^`^`^`text>> doc\test_results.md && python -m pytest --verbose >> doc\test_results.md 2>&1 && echo ^`^`^`>> doc\test_results.md"
else
	PYTHON = python3
	NPM = npm
	STOP_BACKEND = fuser -k $(BACKEND_PORT)/tcp 2>/dev/null || pkill -f "uvicorn.*$(BACKEND_PORT)" || echo Backend detenido
	STOP_FRONTEND = fuser -k $(FRONTEND_PORT)/tcp 2>/dev/null || pkill -f "vite" || echo Frontend detenido
	SLEEP = sleep 3
	RUN_BACKEND = $(PYTHON) -m uvicorn main:app --reload --port $(BACKEND_PORT)
	RUN_TESTS = echo "# Reporte de Pruebas Unitarias Autogenerado" && echo "Fecha de ejecución: $$(date)" && echo "\`\`\`text" && python3 -m pytest --verbose && echo "\`\`\`" && mkdir -p doc && echo "# Reporte de Pruebas Unitarias Autogenerado" > doc/test_results.md && echo "Fecha de ejecución: $$(date)" >> doc/test_results.md && echo "\`\`\`text" >> doc/test_results.md && python3 -m pytest --verbose >> doc/test_results.md 2>&1 || true && echo "\`\`\`" >> doc/test_results.md
endif

up: ## Lanzar backend y frontend simultáneamente
	@echo "🚀 Iniciando servicios..."
	@$(STOP_BACKEND)
	@$(STOP_FRONTEND)
	@$(SLEEP)
ifeq ($(OS),Windows_NT)
	@start "Backend - Gastos" cmd /c "cd /d $(BACKEND_DIR) && $(RUN_BACKEND)"
	@cd $(FRONTEND_DIR) && $(NPM) run dev
else
	@cd $(BACKEND_DIR) && nohup $(RUN_BACKEND) > ../backend.log 2>&1 & echo $$! > ../backend.pid
	@cd $(FRONTEND_DIR) && $(NPM) run dev
endif

down: ## Detener todos los servicios
	@echo "🛑 Deteniendo servicios..."
	@$(STOP_BACKEND)
	@$(STOP_FRONTEND)
	@echo "✅ Todos los servicios detenidos"

test: ## Ejecutar pruebas unitarias/integración
ifeq ($(OS),Windows_NT)
	@if not exist $(BACKEND_DIR)\doc mkdir $(BACKEND_DIR)\doc
	@cd $(BACKEND_DIR) && $(RUN_TESTS)
else
	@cd $(BACKEND_DIR) && $(RUN_TESTS)
endif
