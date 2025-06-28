import sqlite3
import pandas as pd
import plotly.express as px
    
DB_PATH = "db/pavement.db"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM segments", conn)
    conn.close()
    return df

def plot_pci_distribution(df):
    fig = px.histogram(df, x="pci", nbins=30,
                       title="Distribución del Índice de Condición del Pavimento (PCI)",
                       labels={"pci": "PCI"})
    fig.update_layout(xaxis_title="PCI", yaxis_title="Frecuencia")
    return fig

def plot_aadt_by_road_type(df):
    df_grouped = df.groupby("road_type")["aadt"].mean().reset_index()
    fig = px.bar(df_grouped, x="road_type", y="aadt",
                 title="Promedio de AADT por Tipo de Carretera",
                 labels={"road_type": "Tipo de Carretera", "aadt": "AADT Promedio"})
    return fig

def plot_iri_vs_maintenance(df):
    fig = px.box(df, x="needs_maintenance", y="iri",
                 title="IRI según Necesidad de Mantenimiento",
                 labels={"needs_maintenance": "¿Necesita Mantenimiento? (0 = No, 1 = Sí)", "iri": "IRI (m/km)"})
    return fig



