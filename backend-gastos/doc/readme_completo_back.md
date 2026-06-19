# Manual Técnico del Backend (FastAPI)

Este documento detalla la arquitectura, endpoints y la estructura técnica de la API REST para el mini gestor de gastos.

## Arquitectura

El backend está desarrollado sobre **FastAPI** en Python y utiliza **Pydantic** para la validación de tipos y esquemas de datos. Los datos se persisten localmente en un archivo JSON.

### Endpoints de la API

Todos los endpoints están prefijados bajo la ruta base `/api/gastos`:

1. **`POST /api/gastos`**:
   - Registra un nuevo gasto.
   - Valida que el importe sea mayor que `0` y que los campos requeridos estén presentes.
   - Retorna el gasto guardado junto con un UUID único generado de forma automática si no fue enviado.

2. **`GET /api/gastos`**:
   - Recupera el listado completo de gastos.
   - Parámetros de consulta opcionales para filtrado desde el servidor:
     * `categoria`: Filtra los gastos que contienen la categoría indicada (case-insensitive).
     * `fecha_inicio`: Filtra gastos con fecha igual o posterior a `YYYY-MM-DD`.
     * `fecha_fin`: Filtra gastos con fecha igual o anterior a `YYYY-MM-DD`.

3. **`PUT /api/gastos/{gasto_id}`**:
   - Actualiza un registro existente mediante su ID.
   - Retorna el objeto actualizado.

4. **`DELETE /api/gastos/{gasto_id}`**:
   - Elimina un registro de gasto por su ID.
   - Retorna un código HTTP `204 No Content` al realizar la operación con éxito.

## Persistencia de Datos

- Los datos se almacenan en el archivo local `database.json`.
- En caso de no existir o estar vacío al arrancar la aplicación, se inicializa automáticamente.

## Ejecución de Pruebas (Tests)

Las pruebas están escritas con `pytest` y cubren validaciones de API, inserciones, actualizaciones, filtrados y eliminaciones.
Para correr las pruebas e inicializar el reporte automático:
```bash
.\make test
```
El resultado detallado e histórico de los tests se actualiza automáticamente en el fichero:
- [test_results.md](file:///d:/Users/proyecto-gastos-qdq/backend-gastos/doc/test_results.md)

## Ejecución del Servidor de Desarrollo

Para levantar el servidor en el puerto 8000 con recarga automática:

```bash
uvicorn main:app --reload --port 8000
```
