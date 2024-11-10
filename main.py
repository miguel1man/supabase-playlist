from fastapi import FastAPI
from routes.songs import router as songs_router

app = FastAPI()


@app.get("/")
async def root():
    """
    # Ruta raíz que retorna la versión de la API
    """
    return {"version": "0.1"}


app.include_router(songs_router)
