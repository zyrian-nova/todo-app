"""
Rutas de la API para las operaciones CRUD de las tareas
"""
from typing import List
from fastapi import APIRouter,HTTPException,status
from api.models.todo import Todo
from api.schemas.todo import GeneratedSubtasks, GetTodo,PostTodo,PutTodo
from api.services.todo import AIService
from tortoise.contrib.fastapi import DoesNotExist

# Prefijo 'api/' y etiqueta para la documentación
todo_router = APIRouter(prefix="/api", tags=["Todo"])

# Inicializa el servicio de IA
ai_service = AIService()

# Obtiene todas las tareas
@todo_router.get("/", response_model=List[GetTodo])
async def all_todos() -> List[GetTodo]:
    data = Todo.all()
    return await GetTodo.from_queryset(data)

# Crea una nueva tarea
@todo_router.post("/", response_model=GetTodo, status_code=status.HTTP_201_CREATED)
async def post_todo(body: PostTodo) -> GetTodo:
    # Crea la tarea con los datos del body
    row = await Todo.create(**body.model_dump(exclude_unset=True))
    return await GetTodo.from_tortoise_orm(row)

# Actualiza una tarea existente
@todo_router.put("/{key}", response_model=GetTodo)
async def update_todo(key: int,body: PutTodo) -> GetTodo:
    try:
        # Obtener tarea
        db_todo = await Todo.get(id=key)

        # Actualizar tarea
        update_data = body.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)

        # Guardar cambios
        await db_todo.save()

        # Se retorna el objeto actualizado
        return await GetTodo.from_tortoise_orm(db_todo)

    except DoesNotExist:
        # Si .get(id=key) no encuentra dana lanza DoesNotExist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada")

# Elimina una tarea
@todo_router.delete("/{key}", status_code=status.HTTP_200_OK)
async def delete_todo(key: int) -> dict[str, str]:
    # Intentamos eliminar la tarea
    deleted_count = await Todo.filter(id=key).delete()
    if not deleted_count:
        # Si no eliminó, envía un mensaje de que no se encontró
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada")
    return {"message": "Tarea eliminada exitosamente"}

# Genera subtareas automáticamente usando la IA
@todo_router.post("/{key}/generate-subtasks", response_model=GeneratedSubtasks)
async def generate_subtasks(key: int) -> GeneratedSubtasks:
    # Verifica que la tarea exista
    try:
        main_task = await Todo.get(id=key)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada")

    try:
        # Genera las subtareas usando IA
        subtask_texts = ai_service.generate_subtasks(main_task.task)

        # Crea las subtareas en la base de datos, especificamos que es una lista de 'GetTodo'
        created_subtasks: List[GetTodo] = []
        for subtask_text in subtask_texts:
            # Asegura que sea un string y limita a 100 caracteres
            task_str = str(subtask_text).strip()[:100]
            subtask = await Todo.create(
                task=task_str,
                done=False,
                parent_task_id=key
            )
            #created_subtasks.append(await GetTodo.from_tortoise_orm(subtask))
            pydantic_subtask = await GetTodo.from_tortoise_orm(subtask)
            created_subtasks.append(pydantic_subtask)

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
async def get_subtasks(key: int) -> List[GetTodo]:
    # Verifica que la tarea exista
    exists = await Todo.filter(id=key).exists()
    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Tarea no encontrada")
    # Obtiene las subtareas
    subtasks = Todo.filter(parent_task_id=key)
    return await GetTodo.from_queryset(subtasks)
