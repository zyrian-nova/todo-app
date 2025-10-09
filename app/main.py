"""
Configuración principal de la aplicación FastAPI
"""
from fastapi import FastAPI
from api.routes.todo import todo_router
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

# Inicializa la aplicación
app = FastAPI()

# Registra las rutas
app.include_router(todo_router)

# Headers CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configura el ORM Tortoise con SQLite
register_tortoise(
    app=app,
    db_url="sqlite://todo.db",
    add_exception_handlers=True, # Maneja excepciones de la BD
    generate_schemas=True, # Crea tablas automáticamente si no existen
    modules={"models":["api.models.todo"]} # Carga los modelos
)

# Endpoint raíz para verificar el estado de la API
@app.get("/")
def index():
    return {"status": "La aplicación ToDo está corriendo..."}
