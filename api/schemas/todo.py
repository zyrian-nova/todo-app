"""
Esquemas Pydantic para validación y serialización de tareas
"""
from pydantic import BaseModel,Field
from tortoise.contrib.pydantic import pydantic_model_creator
from api.models.todo import Todo

# Schema automático para respuestas (GET) generado desde el modelo Tortoise
GetTodo = pydantic_model_creator(Todo, name="ToDo")

# Schema para crear una nueva tarea (POST)
class PostTodo(BaseModel):
    task:str = Field(...,max_length=100) # Obligatorio
    done:bool # Obligatorio

# Schema para actualizar una tarea existente (PUT)
class PutTodo(BaseModel):
    task: str | None = Field(None, max_length=100) # Opcional
    done: bool | None # Opcional
