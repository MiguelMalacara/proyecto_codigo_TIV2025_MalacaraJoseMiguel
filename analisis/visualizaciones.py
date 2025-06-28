import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DB_PATH = "db/pavement.db"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM segments", conn)
    conn.close()
    return df

def plot_pci_distribution(df):
    plt.figure(figsize=(8, 5))
    sns.histplot(df["pci"], bins=30, kde=True, color='skyblue')
    plt.title("Distribución del Índice de Condición del Pavimento (PCI)")
    plt.xlabel("PCI")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig("pci_distribution.png")
    plt.close()

def plot_aadt_by_road_type(df):
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="road_type", y="aadt", estimator='mean', ci=None, palette="Set2")
    plt.title("Promedio de AADT por Tipo de Carretera")
    plt.xlabel("Tipo de Carretera")
    plt.ylabel("AADT Promedio")
    plt.tight_layout()
    plt.savefig("aadt_by_road_type.png")
    plt.close()

def plot_iri_vs_maintenance(df):
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="needs_maintenance", y="iri", palette="Set1")
    plt.title("IRI según Necesidad de Mantenimiento")
    plt.xlabel("¿Necesita Mantenimiento? (0 = No, 1 = Sí)")
    plt.ylabel("IRI (m/km)")
    plt.tight_layout()
    plt.savefig("iri_vs_maintenance.png")
    plt.close()

if __name__ == "__main__":
    df = load_data()
    plot_pci_distribution(df)
    plot_aadt_by_road_type(df)
    plot_iri_vs_maintenance(df)
    print("Visualizaciones generadas y guardadas como imágenes.")
