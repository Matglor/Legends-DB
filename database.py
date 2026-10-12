import sqlite3

def inicializar_bd():
    # Conexión a la base de datos de Dragon Ball Legends Local
    con = sqlite3.connect('dragonball.db')
    cur = con.cursor()

    # 1. Crear tabla de Rarezas (Rarities)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Rarity (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );""")

    # 2. Crear tabla de Tipos / Elementos (Types)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Type (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );""")

    # 3. Crear tabla de Tags (Etiquetas de los personajes)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Tag (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE
    );""")

    # 4. Crear tabla principal de Personajes (Characters)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Character (
        id TEXT PRIMARY KEY,               -- Ejemplo: 'DBL55-01S'
        nombre TEXT NOT NULL,              -- Ejemplo: 'Super Saiyan Goku'
        rarity_id INTEGER,
        type_id INTEGER,
        es_zenkai INTEGER DEFAULT 0,       -- 0 = No, 1 = Sí
        es_lf_ll INTEGER DEFAULT 0,         -- 0 = No, 1 = Sí
        CONSTRAINT fk_char_rarity FOREIGN KEY (rarity_id) REFERENCES Rarity (id),
        CONSTRAINT fk_char_type FOREIGN KEY (type_id) REFERENCES Type (id)
    );""")

    # 5. Crear tabla intermedia Muchos a Muchos (Character_Tags)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Character_Tag (
        character_id TEXT,
        tag_id INTEGER,
        PRIMARY KEY (character_id, tag_id),
        CONSTRAINT fk_ct_character FOREIGN KEY (character_id) REFERENCES Character (id) ON DELETE CASCADE,
        CONSTRAINT fk_ct_tag FOREIGN KEY (tag_id) REFERENCES Tag (id) ON DELETE CASCADE
    );""")

    # --- INSERCIÓN DE DATOS SEMILLA BASE ---
    # Rarezas por defecto
    rarezas = [('LEGEND',), ('ULTRA',), ('SPARKING',), ('EXTREME',), ('HERO',)]
    cur.executemany("INSERT OR IGNORE INTO Rarity (nombre) VALUES (?);", rarezas)

    # Tipos por defecto
    tipos = [('RED',), ('BLU',), ('GRN',), ('YEL',), ('PUR',), ('LGT',), ('DRK',)]
    cur.executemany("INSERT OR IGNORE INTO Type (nombre) VALUES (?);", tipos)

    # Algunos Tags de ejemplo populares para empezar
    tags = [('Saiyan',), ('Android',), ('Future',), ('Lineage of Evil',), ('Son Family',), ('Vegeta Clan',)]
    cur.executemany("INSERT OR IGNORE INTO Tag (nombre) VALUES (?);", tags)

    # Confirmar cambios y cerrar conexión
    con.commit()
    con.close()
    print("¡Base de datos 'dragonball.db' inicializada con éxito con datos semilla!")

if __name__ == "__main__":
    inicializar_bd()
