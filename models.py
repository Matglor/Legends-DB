from pydantic import BaseModel, Field
from typing import List, Optional

# --- Modelos de Catálogo (Semilla) ---

class RarityModel(BaseModel):
    id: Optional[int] = None
    nombre: str

class TypeModel(BaseModel):
    id: Optional[int] = None
    nombre: str

class TagModel(BaseModel):
    id: Optional[int] = None
    nombre: str


# --- Modelos del Personaje (Character) ---

# Modelo base para los atributos comunes
class CharacterBase(BaseModel):
    id: str = Field(..., description="Identificador único del personaje, ej: DBL55-01S")
    nombre: str = Field(..., description="Nombre del personaje, ej: Super Saiyan Goku")
    rarity_id: int = Field(..., description="ID de la rareza asociada")
    type_id: int = Field(..., description="ID del tipo/elemento asociado")
    es_zenkai: int = Field(0, description="0 = No tiene Zenkai, 1 = Sí tiene Zenkai")
    es_lf_ll: int = Field(0, description="0 = No es Legends Limited, 1 = Sí es Legends Limited")

# Modelo para CREAR o ACTUALIZAR un personaje (Recibe una lista de IDs de etiquetas)
class CharacterCreate(CharacterBase):
    tags_ids: List[int] = Field([], description="Lista de IDs de los Tags asignados al personaje")

# Modelo extendido para MOSTRAR la información completa (Incluye los nombres resueltos)
class CharacterResponse(CharacterBase):
    rarity_nombre: Optional[str] = None
    type_nombre: Optional[str] = None
    tags: List[str] = Field([], description="Lista con los nombres de las etiquetas del personaje")

    class Config:
        from_attributes = True
