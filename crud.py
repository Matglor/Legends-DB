import sqlite3
from typing import List, Optional
from models import CharacterCreate, CharacterResponse


import os
import sqlite3
from pathlib import Path
from typing import List, Optional
from models import CharacterCreate, CharacterResponse

DATABASE = os.getenv(
    "DATABASE_PATH",
    str(Path(__file__).resolve().parent / "dragonball.db")
)

def conectar_bd():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def conectar_bd():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conn

# --- OPERACIONES CRUD PARA PERSONAJES ---

# 1. CREATE / UPDATE (Guardar o Reemplazar Personaje)
def guardar_personaje(item: CharacterCreate) -> bool:
    conn = conectar_bd()
    cur = conn.cursor()
    try:
        # Usamos INSERT OR REPLACE para cubrir la creación y la edición en una sola lógica
        cur.execute("""
            INSERT OR REPLACE INTO Character (id, nombre, rarity_id, type_id, es_zenkai, es_lf_ll)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (item.id, item.nombre, item.rarity_id, item.type_id, item.es_zenkai, item.es_lf_ll))
        
        # Primero limpiamos las etiquetas anteriores por si es una actualización
        cur.execute("DELETE FROM Character_Tag WHERE character_id = ?;", (item.id,))
        
        # Insertamos las nuevas etiquetas asociadas
        if item.tags_ids:
            relaciones = [(item.id, tag_id) for tag_id in item.tags_ids]
            cur.executemany("""
                INSERT INTO Character_Tag (character_id, tag_id)
                VALUES (?, ?);
            """, relaciones)
            
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error al guardar personaje: {e}")
        return False
    finally:
        conn.close()

# 2. READ (Obtener todos los personajes con sus relaciones resueltas)
def obtener_personajes() -> List[CharacterResponse]:
    conn = conectar_bd()
    cur = conn.cursor()
    lista_personajes = []
    try:
        # Consulta principal con JOIN para traer el nombre de la rareza y el tipo
        cur.execute("""
            SELECT c.id, c.nombre, c.rarity_id, c.type_id, c.es_zenkai, c.es_lf_ll,
                   r.nombre AS rarity_nombre, t.nombre AS type_nombre
            FROM Character c
            LEFT JOIN Rarity r ON c.rarity_id = r.id
            LEFT JOIN Type t ON c.type_id = t.id;
        """)
        personajes_rows = cur.fetchall()

        for row in personajes_rows:
            # Para cada personaje, buscamos sus etiquetas (Tags) correspondientes
            cur.execute("""
                SELECT tg.nombre 
                FROM Character_Tag ct
                JOIN Tag tg ON ct.tag_id = tg.id
                WHERE ct.character_id = ?;
            """, (row["id"],))
            tags_rows = cur.fetchall()
            lista_tags = [t_row["nombre"] for t_row in tags_rows]

            # Construimos el objeto de respuesta estructurado
            obj = CharacterResponse(
                id=row["id"],
                nombre=row["nombre"],
                rarity_id=row["rarity_id"],
                type_id=row["type_id"],
                es_zenkai=row["es_zenkai"],
                es_lf_ll=row["es_lf_ll"],
                rarity_nombre=row["rarity_nombre"],
                type_nombre=row["type_nombre"],
                tags=lista_tags
            )
            lista_personajes.append(obj)
            
        return lista_personajes
    except sqlite3.Error as e:
        print(f"Error al obtener personajes: {e}")
        return []
    finally:
        conn.close()

# 3. DELETE (Eliminar personaje)
def eliminar_personaje(character_id: str) -> bool:
    conn = conectar_bd()
    cur = conn.cursor()
    try:
        # Al eliminar el personaje, SQLite limpiará la tabla intermedia gracias al ON DELETE CASCADE
        cur.execute("DELETE FROM Character WHERE id = ?;", (character_id,))
        conn.commit()
        # Verificar si realmente se eliminó algún registro
        return cur.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error al eliminar personaje: {e}")
        return False
    finally:
        conn.close()


# --- FUNCIONES AUXILIARES PARA POBLAR LOS FILTROS DEL FRONTEND ---

def obtener_raridades() -> List[dict]:
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM Rarity;")
    rows = cur.fetchall()
    conn.close()
    return [{"id": row["id"], "nombre": row["nombre"]} for row in rows]

def obtener_tipos() -> List[dict]:
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM Type;")
    rows = cur.fetchall()
    conn.close()
    return [{"id": row["id"], "nombre": row["nombre"]} for row in rows]

def obtener_tags() -> List[dict]:
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM Tag;")
    rows = cur.fetchall()
    conn.close()
    return [{"id": row["id"], "nombre": row["nombre"]} for row in rows]
