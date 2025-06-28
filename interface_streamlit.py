import streamlit as st
import pandas as pd
import plotly.express as px
import visualizaciones
import database

st.set_page_config(page_title="Pavimento", page_icon="🛣️", layout="wide")

class AppPavimento:
    def __init__(self):
        try:
            self.df = pd.DataFrame(database.get_segments())
        except Exception as e:
            st.error(f"Error al cargar datos: {e}")
            self.df = pd.DataFrame()

    def vista_registro_segmento(self):
        st.title("📝 Registro de segmento vial")
        st.write("Por favor, rellene los siguientes campos:")

        with st.form("form_segmento"):
            col1, col2 = st.columns(2)
            with col1:
                segment_id = st.text_input("ID del segmento:")
                pci = st.slider("PCI (0-100):", min_value=0, max_value=100, value=50)
                road_type = st.selectbox("Tipo de carretera:", ["Primary", "Secondary", "Tertiary"])
                aadt = st.number_input("AADT (tráfico diario promedio):", min_value=0, step=100)
                asphalt_type = st.selectbox("Tipo de asfalto:", ["Dense", "Open-graded", "SMA", "Asphalt", "Concrete"])
            with col2:
                last_maintenance = st.number_input("Año del último mantenimiento:", min_value=1900, max_value=2100, value=2020)
                average_rainfall = st.number_input("Lluvia anual promedio (mm):", min_value=0.0, step=1.0)
                rutting = st.number_input("Rutting (mm):", min_value=0.0, step=0.1)
                iri = st.number_input("IRI (m/km):", min_value=0.0, step=0.01)
                needs_maintenance = st.selectbox("¿Requiere mantenimiento?", [0, 1])

            enviado = st.form_submit_button("Guardar segmento")

            if enviado:
                nuevo = {
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
                    database.insert_segment(nuevo)
                    st.success(f"Segmento {segment_id} guardado exitosamente.")
                except Exception as e:
                    st.error(f"Error al guardar el segmento: {e}")

    def vista_consulta_segmentos(self):
        st.title("🔍 Consulta de segmentos")
        condicion = st.text_input("Condición SQL (opcional):", placeholder="Ej: needs_maintenance = 1")
        try:
            data = database.get_segments(condicion if condicion else None)
            df = pd.DataFrame(data)
            if not df.empty:
                st.success("Segmentos recuperados exitosamente")
                st.dataframe(df)
            else:
                st.info("No hay segmentos registrados")
        except Exception as e:
            st.error(f"Error al consultar la base de datos: {e}")

    def vista_visualizaciones(self):
        st.title("📊 Visualizaciones")
        if self.df.empty:
            st.info("No hay datos disponibles para graficar.")
            return

        st.plotly_chart(visualizaciones.plot_pci_distribution(self.df), use_container_width=True)
        st.plotly_chart(visualizaciones.plot_aadt_by_road_type(self.df), use_container_width=True)
        st.plotly_chart(visualizaciones.plot_iri_vs_maintenance(self.df), use_container_width=True)

    def run(self):
        st.sidebar.title("Menú")
        opcion = st.sidebar.selectbox("Ir a:", ["Registro", "Consulta", "Gráficas"])
        if opcion == "Registro":
            self.vista_registro_segmento()
        elif opcion == "Consulta":
            self.vista_consulta_segmentos()
        elif opcion == "Gráficas":
            self.vista_visualizaciones()

app = AppPavimento()
app.run()

