from typing import Tuple
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from .interfaces import DocumentRepository, DocumentMetadata
from .config import VisualizationConfig

class DocumentVisualizer:
    def __init__(self, repository: DocumentRepository, config: VisualizationConfig | None = None):
        """
        Initialize the document visualizer.
        
        Args:
            repository: Repository to fetch documents from
            config: Visualization configuration. If None, uses default settings.
        """
        self.repository = repository
        self.config = config or VisualizationConfig()
        
    def _prepare_data(self, embedding_type) -> Tuple[np.ndarray, pd.DataFrame]:
        """
        Prepare data for visualization.
        
        Returns:
            Tuple of (scaled embeddings array, metadata dataframe)
        """
        # Get documents and extract metadata
        documents = self.repository.get_documents(embedding_type)
        metadata = [
            DocumentMetadata(
                path=doc.path,
                title=doc.title,
                authors=doc.authors,
                topic=doc.topic,
                embedding=doc.embedding.get_vector()
            )
            for doc in documents
        ]
        
        # Create embeddings array and metadata dataframe
        embeddings = np.array([m.embedding for m in metadata])
        df = pd.DataFrame({
            'Path': [m.path for m in metadata],
            'Name': [m.title for m in metadata],
            'Author': [", ".join(m.authors) for m in metadata],
            'Category': [m.topic for m in metadata]
        })
        
        # Scale the embeddings
        scaler = StandardScaler()
        embeddings_scaled = scaler.fit_transform(embeddings)
        
        return embeddings_scaled, df
        
    def _perform_dimensionality_reduction(
        self, 
        data: np.ndarray
    ) -> Tuple[np.ndarray, str, str]:
        """
        Perform dimensionality reduction on the data.
        
        Returns:
            Tuple of (reduced data, x-axis label, y-axis label)
        """
        if self.config.dim_reduction == "PCA":
            reducer = PCA(n_components=2)
            reduced_data = reducer.fit_transform(data)
            x_label, y_label = "PCA Component 1", "PCA Component 2"
        else:  # TSNE
            reducer = TSNE(n_components=2, perplexity=min(30, len(data)-1))
            reduced_data = reducer.fit_transform(data)
            x_label, y_label = "t-SNE Component 1", "t-SNE Component 2"
            
        return reduced_data, x_label, y_label
        
    def create_cluster_visualization(
        self,
        embedding_type,
        cut_height: float | None = None
    ) -> Tuple[plt.Figure, plt.Figure, pd.DataFrame]:
        """
        Create the cluster visualization.
        
        Args:
            embedding_type: Type of embedding to use
            cut_height: Height to cut the dendrogram. If None, uses config value.
            
        Returns:
            Tuple of (dendrogram figure, scatter plot figure, metadata dataframe)
        """
        # Prepare data
        data_scaled, metadata = self._prepare_data(embedding_type)
        
        # Calculate linkage matrix
        Z = linkage(data_scaled, method=self.config.linkage_method)
        
        # Determine cut height if not provided
        if cut_height is None:
            cut_height = (self.config.cut_height if self.config.cut_height is not None 
                         else self.config.get_default_cut_height(Z))
        
        # Get clusters
        clusters = fcluster(Z, t=cut_height, criterion='distance')
        metadata['Cluster'] = clusters.astype(str)
        n_clusters = len(np.unique(clusters))
        
        # Create color mapping
        cluster_colors = {
            str(i): self.config.colors[i % len(self.config.colors)]
            for i in range(1, n_clusters + 1)
        }
        
        # Create dendrogram
        dendro_fig, dendro_ax = plt.subplots(figsize=(10, 6))
        dendrogram(
            Z,
            ax=dendro_ax,
            orientation='top',
            color_threshold=cut_height,
            above_threshold_color='gray',
            no_labels=True
        )
        dendro_ax.axhline(y=cut_height, color='r', linestyle='--')
        dendro_ax.set_title(f"Dendrogram ({self.config.linkage_method})")
        dendro_ax.set_ylabel("Distance")
        
        # Add legend
        handles = [plt.Rectangle((0,0),1,1, color=self.config.colors[i]) 
                  for i in range(n_clusters)]
        dendro_ax.legend(
            handles, 
            [f"Cluster {i+1}" for i in range(n_clusters)],
            title="Clusters",
            bbox_to_anchor=(1.05, 1),
            loc='upper left'
        )
        
        # Perform dimensionality reduction
        vis_data, x_label, y_label = self._perform_dimensionality_reduction(data_scaled)
        metadata['x'] = vis_data[:, 0]
        metadata['y'] = vis_data[:, 1]
        
        # Create scatter plot
        scatter_fig = px.scatter(
            metadata,
            x='x',
            y='y',
            color='Cluster',
            color_discrete_map=cluster_colors,
            hover_name='Name',
            hover_data=['Author', 'Category'],
            title=f"Clusters found: {n_clusters}"
        )
        scatter_fig.update_layout(
            xaxis_title=x_label,
            yaxis_title=y_label,
            legend_title_text='Cluster'
        )
        
        return dendro_fig, scatter_fig, metadata 
