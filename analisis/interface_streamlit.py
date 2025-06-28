import streamlit as st
import pandas as pd
import database
import os

st.title("🚧 Monitoreo de Pavimento y Mantenimiento Vial")

menu = st.sidebar.selectbox("Selecciona una opción", [
    "Ingresar nuevo segmento",
    "Consultar segmentos",
    "Visualizaciones"
])

if menu == "Ingresar nuevo segmento":
    st.header("📝 Ingresar nuevo segmento vial")

    with st.form("segment_form"):
        segment_id = st.text_input("ID del segmento")
        pci = st.number_input("PCI (0-100)", min_value=0, max_value=100, value=50)
        road_type = st.selectbox("Tipo de carretera", ["Primary", "Secondary", "Barangay"])
        aadt = st.number_input("AADT (tráfico diario promedio)", min_value=0, value=1000)
        asphalt_type = st.selectbox("Tipo de asfalto", ["Dense", "Open-graded", "SMA"])
        last_maintenance = st.number_input("Año del último mantenimiento", min_value=1900, max_value=2100, value=2020)
        average_rainfall = st.number_input("Lluvia anual promedio (mm)", min_value=0.0, value=800.0)
        rutting = st.number_input("Rutting (mm)", min_value=0.0, value=10.0)
        iri = st.number_input("IRI (m/km)", min_value=0.0, value=1.0)
        needs_maintenance = st.selectbox("¿Requiere mantenimiento?", [0, 1])

        submitted = st.form_submit_button("Guardar segmento")

        if submitted:
            segment = {
                "segment_id": segment_id,
                "pci": pci,
                "road_type": road_type,
                "aadt": aadt,
                "asphalt_type": asphalt_type,
                "last_maintenance": last_maintenance,
                "average_rainfall": average_rainfall,
                "rutting": rutting,
                "iri": iri,
                "needs_maintenance": needs_maintenance
            }
            try:
                database.insert_segment(segment)
                st.success(f"Segmento {segment_id} guardado exitosamente.")
            except Exception as e:
                st.error(f"Error al guardar el segmento: {e}")

elif menu == "Consultar segmentos":
    st.header("🔍 Consulta de segmentos viales")
    condition = st.text_input("Condición SQL (opcional)", placeholder="Ej: needs_maintenance = 1")
    try:
        data = database.get_segments(condition if condition else None)
        df = pd.DataFrame(data)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No se encontraron registros.")
    except Exception as e:
        st.error(f"Error al consultar la base de datos: {e}")

elif menu == "Visualizaciones":
    st.header("📊 Visualizaciones")

    image_files = {
        "Distribución del PCI": "pci_distribution.png",
        "AADT por tipo de carretera": "aadt_by_road_type.png",
        "IRI según mantenimiento": "iri_vs_maintenance.png"
    }

    for title, file in image_files.items():
        if os.path.exists(file):
            st.subheader(title)
            st.image(file)
        else:
            st.warning(f"No se encontró la imagen: {file}")
