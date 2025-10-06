"""
Servicio para interactuar con Ollama (local) o APIs de IA
"""
import json
import os
import logging
import ollama

# Configura logging para debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Configuración de Ollama
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2")

        logger.info(f"Usando Ollama en {self.ollama_host} con modelo {self.ollama_model}")

    def generate_subtasks(self, main_task: str) -> list[str]:
        """
        Genera subtareas específicas basadas en una tarea principal usando Ollama

        Args:
            main_task: Descripción de la tarea principal

        Returns:
            Lista de subtareas generadas
        """
        prompt = f"""Divide esta tarea en 3-5 subtareas específicas y accionables.
Responde SOLO con un JSON válido en este formato exacto, sin explicaciones adicionales:
{{"subtasks": ["subtarea 1", "subtarea 2", "subtarea 3"]}}

Tarea principal: {main_task}

JSON:"""

        try:
            logger.info(f"Generando subtareas para: {main_task}")

            # Llamada a Ollama
            response = ollama.chat(
                model=self.ollama_model,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }],
                options={
                    'temperature': 0.7,
                }
            )

            # Extrae el contenido de la respuesta
            response_text = response['message']['content'].strip()
            logger.info(f"Respuesta de Ollama recibida correctamente")

            # Limpia la respuesta si viene con markdown
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()

            # Intenta encontrar el JSON en la respuesta
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                result = json.loads(json_str)
                subtasks = result.get("subtasks", [])

                logger.info(f"Subtareas generadas exitosamente: {len(subtasks)} tareas")
                return subtasks
            else:
                logger.error("No se encontró JSON válido en la respuesta")
                return ["Error: Respuesta sin formato JSON válido"]

        except json.JSONDecodeError as e:
            logger.error(f"Error al parsear JSON: {str(e)}")
            logger.error(f"Respuesta recibida: {response_text if 'response_text' in locals() else 'N/A'}")
            return ["Error: No se pudo procesar la respuesta de IA"]
        except Exception as e:
            error_msg = repr(e)
            logger.error(f"Error en generate_subtasks: {type(e).__name__} - {error_msg}")
            return ["Error al generar subtareas con IA"]
