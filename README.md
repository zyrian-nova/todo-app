# Todo App

API REST para gestión de tareas (Todo List) construida con FastAPI y Tortoise ORM.

## Características

- CRUD completo de tareas
- Validación de datos con Pydantic
- Base de datos SQLite con Tortoise ORM
- Documentación automática con Swagger UI
- Recarga automática en desarrollo

## Requisitos

- Python 3.10+
- PDM (Python Dependency Manager)

## Instalación

1. **Clonar el repositorio**

```bash
git clone <url-del-repositorio>
cd todo-app
```

2. **Sincronizar dependencias con PDM**

```bash
pdm sync
```

3. **Ejecutar el servidor**

```bash
pdm run python server.py
```

El servidor estará disponible en `http://localhost:8000`

## Documentación API

Una vez el servidor esté corriendo, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/` | Obtener todas las tareas |
| POST | `/api/` | Crear una nueva tarea |
| PUT | `/api/{id}` | Actualizar una tarea |
| DELETE | `/api/{id}` | Eliminar una tarea |

## Estructura del Proyecto

```
todo-app/
├── api/
│   ├── models/
│   │   └── todo.py          # Modelo de datos Tortoise ORM
│   ├── routes/
│   │   └── todo.py          # Rutas de la API
│   └── schemas/
│       └── todo.py          # Esquemas Pydantic
├── app/
│   └── main.py              # Configuración principal de FastAPI
├── server.py                # Punto de entrada de la aplicación
├── pyproject.toml           # Configuración de PDM
└── todo.db                  # Base de datos SQLite (generada automáticamente)
```

## Ejemplos de Uso

### Crear una tarea

```bash
curl -X POST "http://localhost:8000/api/" \
  -H "Content-Type: application/json" \
  -d '{"task": "Comprar leche", "done": false}'
```

### Obtener todas las tareas

```bash
curl -X GET "http://localhost:8000/api/"
```

### Actualizar una tarea

```bash
curl -X PUT "http://localhost:8000/api/1" \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

### Eliminar una tarea

```bash
curl -X DELETE "http://localhost:8000/api/1"
```

## Configuración

El servidor se configura en `server.py`:

- **Host**: `0.0.0.0` (accesible desde cualquier interfaz)
- **Puerto**: `8000`
- **Recarga automática**: Habilitada en desarrollo
- **Base de datos**: SQLite (`todo.db`)

## Modelo de Datos

```python
{
  "id": 1,
  "task": "Comprar leche",
  "done": false
}
```

## Licencia

Este proyecto está bajo la Licencia MIT.
