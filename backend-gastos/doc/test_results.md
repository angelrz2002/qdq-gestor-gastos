# Reporte de Pruebas Unitarias Autogenerado 
Fecha de ejecucion: 19/06/2026 16:42:06,57 
```text 
============================= test session starts =============================
platform win32 -- Python 3.14.0, pytest-9.1.0, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: D:\Users\proyecto-gastos-qdq\backend-gastos
plugins: anyio-4.14.0
collecting ... collected 8 items

tests/test_main.py::test_inicializacion_base_de_datos PASSED             [ 12%]
tests/test_main.py::test_crear_gasto_exitoso PASSED                      [ 25%]
tests/test_main.py::test_listar_y_filtrar_por_categoria PASSED           [ 37%]
tests/test_main.py::test_eliminar_gasto_exitoso PASSED                   [ 50%]
tests/test_main.py::test_error_importe_invalido PASSED                   [ 62%]
tests/test_main.py::test_rotura_tipo_de_dato_importe PASSED              [ 75%]
tests/test_main.py::test_rotura_campos_vacios_obligatorios PASSED        [ 87%]
tests/test_main.py::test_eliminar_id_inexistente_o_malformado PASSED     [100%]

============================== warnings summary ===============================
C:\Users\Angel\AppData\Roaming\Python\Python314\site-packages\fastapi\testclient.py:1
  C:\Users\Angel\AppData\Roaming\Python\Python314\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 8 passed, 1 warning in 0.45s =========================
``` 
