# Proyecto Gastos QDQ

Gestor de gastos personales modular y eficiente con backend en Python (FastAPI) y frontend en Vue.js.

## 📁 Estructura del Proyecto

El espacio de trabajo está organizado de la siguiente manera:

```text
proyecto-gastos-qdq/
├── Makefile                # Tareas automatizadas para Unix/Bash
├── make.bat                # Tareas automatizadas para Windows (CMD/PowerShell)
├── .cursorrules            # Reglas del entorno de desarrollo
├── _doc_inicial/
│   ├── README.md           # Pautas y documentación general del proyecto (este archivo)
│   └── prueba-tecnica-candidato 1.docx # Documento de pautas originales
├── backend-gastos/
│   ├── doc/
│   │   ├── readme_completo_back.md  # Manual técnico detallado del backend
│   │   └── test_results.md          # Reporte autogenerado del resultado de los tests
│   ├── tests/
│   │   └── test_main.py    # Suite de pruebas unitarias (pytest)
│   ├── database.json       # Base de datos persistente local en formato JSON
│   ├── main.py             # Archivo principal de FastAPI
│   └── requirements.txt    # Dependencias de Python
└── frontend-gastos/
    ├── doc/
    │   └── readme_completo_front.md # Manual técnico detallado del frontend
    ├── public/
    │   └── favicon.png     # Favicon de la aplicación
    ├── src/
    │   ├── assets/
    │   │   └── brand-logo.png # Logo de la marca
    │   ├── components/
    │   │   ├── ExpenseForm.vue      # Formulario modal de gastos (añadir/editar)
    │   │   ├── ExpenseList.vue      # Tabla interactiva con filtros y paginación
    │   │   ├── ExpenseSummary.vue   # Resumen de gastos y gráfico por categorías
    │   │   └── CustomDatePicker.vue # Componente selector de fecha reutilizable
    │   ├── App.vue         # Componente raíz de Vue
    │   ├── App.css         # Hoja de estilos global y variables
    │   └── main.js         # Entrada principal de javascript
    ├── package.json        # Configuración de NPM y dependencias
    ├── package-lock.json   # Árbol de dependencias bloqueado de NPM
    ├── vite.config.js      # Configuración del empaquetador Vite
    └── index.html          # Entrada HTML principal de la aplicación client web
```

---

## 🛠️ Cómo Levantar y Desarrollar el Proyecto

Los comandos de automatización se ejecutan mediante `.\make <comando>` (en Windows CMD/PowerShell) o `make <comando>` / `.\make <comando>` (en Unix/Bash).

### 1. Iniciar el Ecosistema Completo (Backend + Frontend)
Levanta la API FastAPI en segundo plano en el puerto `8000` y el servidor de desarrollo de Vite para el frontend en el puerto `5173`.
```bash
.\make up
```

### 2. Detener Servicios y Liberar Puertos
Detiene de forma limpia los procesos de Uvicorn (puerto `8000`) y Vite (puerto `5173`).
```bash
.\make down
```

### 3. Ejecutar Pruebas Unitarias e Integración
Ejecuta la suite de pruebas mediante `pytest`, muestra el reporte formateado en tiempo real en la terminal y actualiza de forma automática el reporte en formato Markdown.
```bash
.\make test
```

---

## ⚠️ Datos Importantes y Reglas de Desarrollo

* **Restricción de Tamaño:** Ningún archivo de código (`.py`, `.vue`, `.js`) puede superar las **800 líneas de código**. Si crece por encima de este límite, refactoriza dividiendo responsabilidades inmediatamente.
* **Resultados de Tests:** El reporte oficial e histórico de pruebas se guarda exclusivamente en `backend-gastos/doc/test_results.md`.
* **Sincronización de Documentación:** Cualquier evolución del código debe actualizarse inmediatamente en sus manuales específicos: `backend-gastos/doc/readme_completo_back.md` y `frontend-gastos/doc/readme_completo_front.md`.
* **Base de Datos Inicial:** Si la base de datos `database.json` no existe o está vacía, el backend se autoinicializa.

---

## 🔧 Resolución de Problemas al Clonar en Windows

Si acabas de clonar el repositorio en un equipo limpio, sigue estos pasos antes de lanzar `.\make up`:

### Paso 1: Preparar el backend (solo la primera vez)
Crea el entorno virtual de Python e instala las dependencias:
```powershell
cd backend-gastos
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
cd ..
```

### Paso 2: Instalar dependencias del frontend (solo la primera vez)
```powershell
cd frontend-gastos
npm install
cd ..
```

### Paso 3: Lanzar el proyecto
```powershell
.\make up
```

---

### ⚠️ Error de políticas de ejecución al activar el `.venv`
Si al ejecutar `.\.venv\Scripts\activate` aparece un error en rojo indicando que la ejecución de scripts está deshabilitada, ejecuta esto primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
```
Después repite el paso 1.


