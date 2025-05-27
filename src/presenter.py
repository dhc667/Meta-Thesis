from pathlib import Path
from sklearn.manifold import TSNE
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from sqlite_repository.sqlite_repository import SQLiteDocumentRepository
from fireworks_api.fireworks_embedding import FireworksEmbedding

# Configure Streamlit page
st.set_page_config(layout="wide")
st.title("Interactive Dendrogram")

repository = SQLiteDocumentRepository(Path("./db"))

# Simulamos los datos ya que no tenemos acceso a tus repositorios
def get_data():
    documents = repository.get_documents(FireworksEmbedding)
    data = [doc.embedding.get_vector() for doc in documents]
    
    # Create metadata for each point
    names = [doc.title for doc in documents]
    authors = [", ".join(doc.authors) for doc in documents]
    categories = [doc.topic for doc in documents]
    
    metadata = pd.DataFrame({
        'Name': names,
        'Author': authors,
        'Category': categories,
    })
    
    return data, metadata

# Definimos la paleta de colores
COLORS = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5"
]

# Sidebar controls
st.sidebar.header("Clustering Parameters")
linkage_method = st.sidebar.selectbox(
    "Linkage Method",
    ["ward", "complete", "average", "single"],
    index=0
)

dim_reduction = st.sidebar.selectbox(
    "Dimensionality Reduction",
    ["PCA", "TSNE"],
    index=0
)

# Cargamos los datos
data, metadata = get_data()

# Estandarizamos los datos
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Calculamos la matriz de linkage
Z = linkage(data_scaled, method=linkage_method)

# Calculamos alturas para el slider
min_cut = float(np.min(Z[:, 2]))
max_cut = float(np.max(Z[:, 2]))
default_cut = min_cut + (max_cut - min_cut) * 0.7

cut_height = st.sidebar.slider(
    "Cut Height",
    min_value=float(min_cut),
    max_value=float(max_cut + 2),
    value=float(default_cut),
    step=(max_cut - min_cut)/100
)

# Obtenemos los clusters
clusters = fcluster(Z, t=cut_height, criterion='distance')
metadata['Cluster'] = clusters.astype(str)
n_clusters = len(np.unique(clusters))

# Reducción de dimensionalidad
if dim_reduction == "PCA":
    reducer = PCA(n_components=2)
    vis_data = reducer.fit_transform(data_scaled)
    x_label, y_label = "Componente PCA 1", "Componente PCA 2"
else:
    reducer = TSNE(n_components=2, perplexity=min(30, len(data_scaled)-1))
    vis_data = reducer.fit_transform(data_scaled)
    x_label, y_label = "Componente t-SNE 1", "Componente t-SNE 2"

metadata['x'] = vis_data[:, 0]
metadata['y'] = vis_data[:, 1]

# Mapeo de clusters a colores
cluster_to_color = {str(i): COLORS[i % len(COLORS)] for i in range(1, n_clusters+1)}

# Creamos las columnas para los gráficos
col1, col2 = st.columns(2)

# Gráfico 1: Dendrograma
with col1:
    st.subheader("Dendrograma")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Personalizamos el dendrograma
    dendro = dendrogram(
        Z,
        ax=ax,
        orientation='top',
        color_threshold=cut_height,
        above_threshold_color='gray',
        no_labels=True  # Ocultamos las etiquetas para evitar sobrecarga
    )
    
    # Línea de corte
    ax.axhline(y=cut_height, color='r', linestyle='--')
    ax.set_title(f"Dendrograma ({linkage_method})")
    ax.set_ylabel("Distancia")
    
    # Leyenda de colores
    handles = [plt.Rectangle((0,0),1,1, color=COLORS[i]) for i in range(n_clusters)]
    ax.legend(handles, [f"Cluster {i+1}" for i in range(n_clusters)], 
              title="Clusters", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    st.pyplot(fig)

# Gráfico 2: Visualización de clusters
with col2:
    st.subheader("Visualización de Clusters")
    
    fig = px.scatter(
        metadata,
        x='x',
        y='y',
        color='Cluster',
        color_discrete_map=cluster_to_color,
        hover_name='Name',
        hover_data=['Author', 'Category'],
        title=f"Clusters encontrados: {n_clusters}"
    )
    
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title_text='Cluster'
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Información adicional
st.subheader("Información de Clusters")
st.write(f"Número de clusters: {n_clusters}")
st.bar_chart(metadata['Cluster'].value_counts())

if st.checkbox("Mostrar metadatos"):
    st.dataframe(metadata)
