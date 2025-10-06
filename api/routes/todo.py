"""
Rutas de la API para las operaciones CRUD de las tareas
"""
from fastapi import APIRouter,HTTPException,status
from api.models.todo import Todo
from api.schemas.todo import GeneratedSubtasks, GetTodo,PostTodo,PutTodo
from api.services.ai_service import AIService

# Prefijo 'api/' y etiqueta para la documentación
todo_router = APIRouter(prefix="/api", tags=["Todo"])

# Inicializa el servicio de IA
ai_service = AIService()

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

# Genera subtareas automáticamente usando la IA
@todo_router.post("/{key}/generate-subtasks", response_model=GeneratedSubtasks)
async def generate_subtasks(key: int):
    # Verifica que la tarea exista
    main_task = await Todo.filter(id=key).first()
    if not main_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada")
    try:
        # Genera las subtareas usando IA
        subtask_texts = ai_service.generate_subtasks(main_task.task)
        # Crea las subtareas en la base de datos
        created_subtasks = []
        for subtask_text in subtask_texts:
            # Asegura que sea un string y limita a 100 caracteres
            task_str = str(subtask_text).strip()[:100]
            subtask = await Todo.create(
                task=task_str,
                done=False,
                parent_task_id=key
            )
            created_subtasks.append(await GetTodo.from_tortoise_orm(subtask))
        # Retorna la respuesta estructurada
        return GeneratedSubtasks(
            main_task_id=main_task.id,
            main_task=main_task.task,
            subtasks=created_subtasks,
            count=len(created_subtasks)
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Error generando subtareas: {str(e)}")

# Obtiene las subtareas de una tarea principal
@todo_router.get("/{key}/subtasks", response_model=list[GetTodo])
async def get_subtasks(key: int):
    # Verifica que la tarea exista
    exists = await Todo.filter(id=key).exists()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada")
    # Obtiene las subtareas
    subtasks = Todo.filter(parent_task_id=key)
    return await GetTodo.from_queryset(subtasks)
