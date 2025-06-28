import database

# Crear la tabla 'segments' si no existe
database.create_table()

# Insertar un segmento de prueba
segmento_prueba = {
    "segment_id": "SEG001",
    "pci": 78,
    "road_type": "Primary",
    "aadt": 12000,
    "asphalt_type": "Dense",
    "last_maintenance": 2018,
    "average_rainfall": 850.5,
    "rutting": 12.3,
    "iri": 0.85,
    "needs_maintenance": 0
}

# Insertar el segmento
database.insert_segment(segmento_prueba)

# Consultar todos los segmentos
segmentos = database.get_segments()

# Mostrar los resultados en consola
print("Segmentos registrados en la base de datos:")
for seg in segmentos:
    print(seg)

