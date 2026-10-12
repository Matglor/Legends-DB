from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

# Importamos nuestros archivos locales
import crud
from models import CharacterCreate, CharacterResponse

app = FastAPI(
    title="Dragon Ball Legends Database - API",
    description="Backend para la administración del catálogo de personajes de Dragon Ball Legends.",
    version="1.0.0"
)

# Montamos la carpeta estática una única vez
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- ENDPOINTS PARA LOS FILTROS Y CATÁLOGOS DINÁMICOS ---

@app.get("/api/rarities", summary="Obtener el catálogo de rarezas disponibles")
def get_rarities():
    return crud.obtener_raridades()

@app.get("/api/types", summary="Obtener el catálogo de tipos/colores disponibles")
def get_types():
    return crud.obtener_tipos()

@app.get("/api/tags", summary="Obtener el catálogo de etiquetas disponibles")
def get_tags():
    return crud.obtener_tags()


# --- ENDPOINTS CRUD DE PERSONAJES ---

@app.get("/api/characters", response_model=list[CharacterResponse], summary="Obtener todos los personajes registrados")
def get_characters():
    return crud.obtener_personajes()

@app.put("/api/characters", status_code=status.HTTP_200_OK, summary="Registrar o actualizar un personaje")
def save_character(character: CharacterCreate):
    exito = crud.guardar_personaje(character)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al procesar o guardar el personaje en la base de datos."
        )
    return {"mensaje": "Personaje guardado de forma exitosa", "character_id": character.id}

@app.delete("/api/characters/{character_id}", summary="Eliminar un personaje por su ID")
def delete_character(character_id: str):
    exito = crud.eliminar_personaje(character_id)
    if not exito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún personaje con el ID '{character_id}' para eliminar."
        )
    return {"mensaje": f"Personaje '{character_id}' eliminado exitosamente"}



# --- RUTAS PARA SERVIR EL FRONTEND ---

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def render_index():
    index_path = BASE_DIR / "index.html"

    if index_path.exists():
        return FileResponse(index_path)

    raise HTTPException(
        status_code=404,
        detail="No se encontró index.html en la carpeta principal."
    )


@app.get("/add-character", response_class=HTMLResponse, include_in_schema=False)
@app.get("/add-character.html", response_class=HTMLResponse, include_in_schema=False)
def add_character_page():
    page_path = BASE_DIR / "add-character.html"

    if page_path.exists():
        return FileResponse(page_path)

    raise HTTPException(
        status_code=404,
        detail=f"No se encontró add-character.html en: {BASE_DIR}"
    )
