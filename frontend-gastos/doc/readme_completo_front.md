# Manual Técnico del Frontend (Vite + Vue 3)

Este documento detalla la arquitectura, los componentes y la estructura técnica del cliente frontend para el gestor de gastos.

## Arquitectura

El frontend está desarrollado sobre **Vue 3** utilizando la **Composition API** con la sintaxis simplificada `<script setup>`. Se compila y sirve usando **Vite**.

### Componentes Principales

1. **`App.vue`**:
   - Componente principal y orquestador del estado de datos global (`gastos`, `cargando`, `error`, `gastoParaEditar`).
   - Implementa llamadas HTTP/Fetch a la API del backend (`http://localhost:8000/api/gastos`).
   - Controla la visualización del modal glassmórfico de añadir/editar mediante transiciones animadas de Vue y maneja los avisos flotantes (Toast).

2. **`ExpenseSummary.vue`**:
   - Calcula el total acumulado de todos los gastos y muestra el conteo.
   - Agrupa los gastos de forma dinámica por categoría, calculando importes acumulados y porcentajes, mostrados como barras de progreso planas con códigos de color personalizados.

3. **`ExpenseForm.vue`**:
   - Formulario interactivo contenido dentro de un modal para la adición y edición de gastos.
   - Utiliza inputs numéricos adaptados que ocultan los controles nativos del navegador.
   - Cuenta con un selector de categoría personalizado con buscador/filtro en línea.
   - Se integra con el componente `<CustomDatePicker>` para el ingreso estilizado de fechas.

4. **`ExpenseList.vue`**:
   - Muestra los gastos en una tabla interactiva estructurada.
   - Cuenta con un panel superior de filtrado que permite buscar por texto en descripción (local), filtrar por categoría usando un selector con buscador integrado, y filtrar por fechas usando el selector de calendario personalizado `<CustomDatePicker>`.
   - Implementa paginación local interactiva, con controles numéricos de páginas y un selector de tamaño de página personalizado (`mini-select`) que se despliega hacia arriba de manera limpia.
   - Muestra botones de acción circulares e iconográficos para editar y borrar registros rápidamente ahorrando espacio en pantalla.

5. **`CustomDatePicker.vue`**:
   - Componente independiente y reutilizable para la selección de fechas.
   - Ofrece un calendario emergente con navegación por mes/año diseñado en armonía con la interfaz oscura del sistema.

## Estilo y Diseño Premium

- **Estética Escura Coherente**: Paleta basada en gris oscuro grafito y acentos en verde corporativo (`#00A859`).
- **Hoja de Estilos Centralizada (`src/App.css`)**: Contiene la definición de variables CSS, tipografía (`Outfit`), scrollbars de todo el sitio, resets del navegador, clases para los selectores interactivos, buscador (`.search-wrapper`, `.search-padding`), botones, modales y animaciones clave. Esto reduce drásticamente el CSS de los componentes Vue para cumplir con el límite de **800 líneas**.
- **Tipografía**: Importada de Google Fonts (`Outfit`).

## Ejecución del Servidor de Desarrollo

Para iniciar el servidor local de desarrollo de Vite:

```bash
cd frontend-gastos
npm run dev
```

Por defecto, la aplicación estará disponible en `http://localhost:5173`.
