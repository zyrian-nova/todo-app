"""
Rutas de la API para las operaciones CRUD de las tareas
"""
from fastapi import APIRouter,HTTPException,status
from api.models.todo import Todo
from api.schemas.todo import GetTodo,PostTodo,PutTodo

# Prefijo 'api/' y etiqueta para la documentación
todo_router = APIRouter(prefix="/api", tags=["Todo"])

# Obtiene todas las tareas
@todo_router.get("/")
async def all_todos():
    data = Todo.all()
    return await GetTodo.from_queryset(data)

# Crea una nueva tarea
@todo_router.post("/")
async def post_todo(body: PostTodo):
    # Crea la tarea con los datos del body
    row = await Todo.create(**body.dict(exclude_unset=True))
    return await GetTodo.from_tortoise_orm(row)

# Actualiza una tarea existente
@todo_router.put("/{key}")
async def update_todo(key: int,body: PutTodo):
    data = body.dict(exclude_unset=True)
    # Verifica que la tarea exista
    exists = await Todo.filter(id=key).exists()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada")
    # Actualiza la tarea
    await Todo.filter(id=key).update(**data)
    return await GetTodo.from_queryset_single(Todo.get(id=key))

# Elimina una tarea
@todo_router.delete("/{key}")
async def delete_todo(key: int):
    # Verifica que la tarea exista
    exists = await Todo.filter(id=key).exists()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada")
    # Elimina la tarea
    await Todo.filter(id=key).delete()
    return "Tarea eliminada exitosamente"
