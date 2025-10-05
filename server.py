"""
Punto de entrada de la aplicación
"""
import uvicorn

if __name__ == "__main__":
    # Inicia el servidor uvicorn
    uvicorn.run(
        "app.main:app", # Ruta al objeto
        host="0.0.0.0", # Todas las interfaces
        port=8000,
        reload=True, # recarga después de guardar
        log_level="info"
    )
