import sqlite3
from typing import List, Dict, Optional

# Ruta de la base de datos
DB_PATH = "db/pavement.db"

def connect():
    """Establece conexión con la base de datos SQLite."""
    return sqlite3.connect(DB_PATH)

def create_table():
    """Crea la tabla 'segments' si no existe."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS segments (
            segment_id TEXT PRIMARY KEY,
            pci INTEGER,
            road_type TEXT,
            aadt INTEGER,
            asphalt_type TEXT,
            last_maintenance INTEGER,
            average_rainfall REAL,
            rutting REAL,
            iri REAL,
            needs_maintenance INTEGER
        );
    """)
    conn.commit()
    conn.close()

def insert_segment(segment: Dict):
    """Inserta un nuevo segmento en la base de datos."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO segments (
            segment_id, pci, road_type, aadt, asphalt_type,
            last_maintenance, average_rainfall, rutting, iri, needs_maintenance
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        segment["segment_id"],
        segment["pci"],
        segment["road_type"],
        segment["aadt"],
        segment["asphalt_type"],
        segment["last_maintenance"],
        segment["average_rainfall"],
        segment["rutting"],
        segment["iri"],
        segment["needs_maintenance"]
    ))
    conn.commit()
    conn.close()

def get_segments(condition: Optional[str] = None) -> List[Dict]:
    """Consulta segmentos con una condición opcional."""
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT * FROM segments"
    if condition:
        query += f" WHERE {condition}"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    columns = [
        "segment_id", "pci", "road_type", "aadt", "asphalt_type",
        "last_maintenance", "average_rainfall", "rutting", "iri", "needs_maintenance"
    ]
    return [dict(zip(columns, row)) for row in rows]

def update_segment(segment_id: str, updates: Dict):
    """Actualiza campos de un segmento por su ID."""
    conn = connect()
    cursor = conn.cursor()
    set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
    values = list(updates.values()) + [segment_id]
    cursor.execute(f"""
        UPDATE segments SET {set_clause} WHERE segment_id = ?;
    """, values)
    conn.commit()
    conn.close()

def delete_segment(segment_id: str):
    """Elimina un segmento por su ID."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM segments WHERE segment_id = ?;", (segment_id,))
    conn.commit()
    conn.close()

# Crear la tabla al importar el módulo
if __name__ == "__main__":
    create_table()
    print("Tabla 'segments' creada o verificada exitosamente.")
