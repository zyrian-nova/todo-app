"""
Esquemas Pydantic para validación y serialización de tareas
"""
from typing import Type, List, TypeVar
from pydantic import BaseModel,Field
from api.models.todo import Todo
from tortoise.queryset import QuerySet
from tortoise.contrib.fastapi import TYPE_CHECKING
from tortoise.contrib.pydantic import pydantic_model_creator

# Schema automático para respuestas (GET) generado desde el modelo Tortoise
# Se utiliza el bloque 'if TYPE_CHECKING:' para que el analizador estático (pyright) entienda
# que 'GetTodo' es un tipo válido.
# Tipo genérico "T"
T = TypeVar("T")

if TYPE_CHECKING:
    # Este código satisface al analizador y ayuda a la documentación en código
    class GetTodo(BaseModel):
        id: int
        task: str
        done: bool
        parent_task_id: int | None = None

    # Métodos de clase dinámicos que usa en 'api/routes/todo'
    @classmethod
    async def from_queryset(cls: Type[T], queryset: "QuerySet[Todo]") -> List[T]:
        ...
    @classmethod
    async def from_tortoise_orm(cls: Type["T"], obj: Todo) -> T:
        ...

else:
    # Código que se ejecuta realmente
    GetTodo = pydantic_model_creator(Todo, name="GetTodo")

# Schema para crear una nueva tarea (POST)
class PostTodo(BaseModel):
    task:str = Field(...,max_length=100) # Obligatorio
    done:bool = Field(default=False)# Obligatorio
    parent_task_id: int | None = Field(None)

# Schema para actualizar una tarea existente (PUT)
class PutTodo(BaseModel):
    task: str | None = Field(None, max_length=100) # Opcional
    done: bool | None # Opcional

# Schema para respuesta de subtareas generadas
class GeneratedSubtasks(BaseModel):
    main_task_id: int
    main_task: str
    subtasks: list[GetTodo]
    count: int
