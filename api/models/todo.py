"""
Modelo de datos para las tareas (ToDos)
"""
from tortoise.models import Model
from tortoise.fields import IntField, BooleanField, CharField

class Todo(Model):
    # Identificador único (Primary Key) autoincrementable
    id = IntField(pk=True)
    # Descripción de la tarea (obligatoria, máximo 100 caracteres)
    task = CharField(max_length=100,null=False)
    # Estado de la tarea (por defecto: False)
    done = BooleanField(default=False)
