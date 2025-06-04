import streamlit as st

from .document_visualizer import DocumentVisualizer
from .config import VisualizationConfig
from .interfaces import DocumentRepository, JsonGenerator, Tokenizer
import numpy as np
from scipy.cluster.hierarchy import linkage
import pandas as pd
from topic_summarizer import TopicSummarizer

class StreamlitPresenter:
    def __init__(self, 
                 repository: DocumentRepository, 
                 json_generator: JsonGenerator,
                 tokenizer: Tokenizer):
        """
        Initialize the Streamlit presenter.
        
        Args:
            repository: Repository to fetch documents from
            json_generator: JSON generator for LLM queries
            tokenizer: Tokenizer for text processing
        """
        self.repository = repository
        self.json_generator = json_generator
        self.tokenizer = tokenizer
        
    def setup_page(self):
        """Configure the Streamlit page."""
        st.set_page_config(layout="wide")
        st.title("Interactive Document Clustering")
        
    def _name_clusters(self, metadata: pd.DataFrame, documents: list, scatter_fig) -> None:
        """
        Name clusters using the topic summarizer and update the existing scatter plot.
        
        Args:
            metadata: DataFrame containing document metadata and cluster assignments
            documents: List of original documents with abstracts
            scatter_fig: The existing plotly scatter plot to update
        """
        # Initialize topic summarizer
        summarizer = TopicSummarizer(
            json_generator=self.json_generator,
            tokenizer=self.tokenizer,
            max_tokens_per_batch=3000
        )
        
        # Create a progress bar
        progress = st.progress(0)
        status_text = st.empty()
        
        # Create a mapping of documents to their abstracts
        doc_abstracts = {doc.path: doc.abstract for doc in documents}
        
        # Get unique clusters
        clusters = metadata['Cluster'].unique()
        total_clusters = len(clusters)
        
        # Add new columns for cluster names and descriptions
        metadata['Cluster_Name'] = ""
        metadata['Cluster_Description'] = ""
        
        # Process each cluster
        for i, cluster in enumerate(clusters):
            status_text.text(f"Naming cluster {i+1} of {total_clusters}...")
            
            # Get abstracts for documents in this cluster
            cluster_docs = metadata[metadata['Cluster'] == cluster]
            cluster_abstracts = [
                doc_abstracts[path] for path in cluster_docs['Path']
                if path in doc_abstracts and doc_abstracts[path]
            ]
            
            if cluster_abstracts:
                # Summarize the cluster's abstracts
                summary = summarizer.summarize_topics(cluster_abstracts)
                
                # Update metadata for all documents in this cluster
                metadata.loc[metadata['Cluster'] == cluster, 'Cluster_Name'] = summary.topic_title
                metadata.loc[metadata['Cluster'] == cluster, 'Cluster_Description'] = summary.topic_description
            else:
                # If no abstracts available, use placeholder
                metadata.loc[metadata['Cluster'] == cluster, 'Cluster_Name'] = f"Cluster {cluster}"
                metadata.loc[metadata['Cluster'] == cluster, 'Cluster_Description'] = "No abstracts available for analysis"
            
            # Update progress
            progress.progress((i + 1) / total_clusters)
        
        # Update the hover data in the existing scatter plot
        scatter_fig.update_traces(
            hovertemplate=(
                "Name: %{customdata[0]}<br>" +
                "Author: %{customdata[1]}<br>" +
                "Category: %{customdata[2]}<br>" +
                "Cluster: %{color}<br>" +
                "Cluster Name: %{customdata[3]}<br>" +
                "Description: %{customdata[4]}<br>" +
                "<extra></extra>"
            ),
            customdata=metadata[['Name', 'Author', 'Category', 'Cluster_Name', 'Cluster_Description']].values
        )
        
        status_text.text("Cluster naming complete!")
        
    def run(self, embedding_type):
        """Run the Streamlit application."""
        self.setup_page()
        
        # Initialize session state for storing the visualization data
        if 'metadata' not in st.session_state:
            st.session_state.metadata = None
        if 'scatter_container' not in st.session_state:
            st.session_state.scatter_container = None
        if 'cluster_summaries' not in st.session_state:
            st.session_state.cluster_summaries = None
        
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
        
        # Create visualizer with current config
        config = VisualizationConfig(
            linkage_method=linkage_method,
            dim_reduction=dim_reduction
        )
        visualizer = DocumentVisualizer(self.repository, config)
        
        # Get initial data to calculate linkage matrix
        data_scaled, metadata = visualizer._prepare_data(embedding_type)
        Z = linkage(data_scaled, method=config.linkage_method)
        
        # Get cut height range and default value
        min_height = float(np.min(Z[:, 2]))
        max_height = float(np.max(Z[:, 2]))
        default_height = config.get_default_cut_height(Z)
        
        # Create cut height slider
        cut_height = st.sidebar.slider(
            "Cut Height",
            min_value=min_height,
            max_value=max_height + (max_height - min_height) * 0.1,  # Add some padding
            value=default_height,
            step=(max_height - min_height)/100
        )
        
        # Create final visualization with user-selected cut height
        dendro_fig, scatter_fig, metadata = visualizer.create_cluster_visualization(
            embedding_type=embedding_type,
            cut_height=cut_height
        )
        
        # Store metadata in session state
        st.session_state.metadata = metadata.copy()
        
        # Display visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dendrogram")
            st.pyplot(dendro_fig)
            
        with col2:
            st.subheader("Cluster Visualization")
            # Create a placeholder for the scatter plot
            st.session_state.scatter_container = st.empty()
            st.session_state.scatter_container.plotly_chart(scatter_fig, use_container_width=True)
        
        # Add name clusters button
        if st.button("Name Clusters Using Topic Analysis"):
            with st.spinner("Analyzing cluster topics..."):
                # Get original documents for their abstracts
                documents = self.repository.get_documents(embedding_type)
                
                # Initialize topic summarizer
                summarizer = TopicSummarizer(
                    json_generator=self.json_generator,
                    tokenizer=self.tokenizer,
                    max_tokens_per_batch=3000
                )
                
                # Create a progress bar
                progress = st.progress(0)
                status_text = st.empty()
                
                # Create a mapping of documents to their abstracts
                doc_abstracts = {doc.path: doc.abstract for doc in documents}
                
                # Get unique clusters
                clusters = st.session_state.metadata['Cluster'].unique()
                total_clusters = len(clusters)
                
                # Initialize cluster summaries dictionary
                cluster_summaries = {}
                
                # Process each cluster
                for i, cluster in enumerate(clusters):
                    status_text.text(f"Naming cluster {i+1} of {total_clusters}...")
                    
                    # Get abstracts for documents in this cluster
                    cluster_docs = st.session_state.metadata[st.session_state.metadata['Cluster'] == cluster]
                    cluster_abstracts = [
                        doc_abstracts[path] for path in cluster_docs['Path']
                        if path in doc_abstracts and doc_abstracts[path]
                    ]
                    
                    if cluster_abstracts:
                        # Summarize the cluster's abstracts
                        summary = summarizer.summarize_topics(cluster_abstracts)
                        cluster_summaries[cluster] = {
                            'name': summary.topic_title,
                            'description': summary.topic_description,
                            'size': len(cluster_docs)
                        }
                    else:
                        # If no abstracts available, use placeholder
                        cluster_summaries[cluster] = {
                            'name': f"Cluster {cluster}",
                            'description': "No abstracts available for analysis",
                            'size': len(cluster_docs)
                        }
                    
                    # Update progress
                    progress.progress((i + 1) / total_clusters)
                
                # Store cluster summaries in session state
                st.session_state.cluster_summaries = cluster_summaries
                
                # Update metadata with cluster names and descriptions
                for cluster, summary in cluster_summaries.items():
                    mask = st.session_state.metadata['Cluster'] == cluster
                    st.session_state.metadata.loc[mask, 'Cluster_Name'] = summary['name']
                    st.session_state.metadata.loc[mask, 'Cluster_Description'] = summary['description']
                
                # Update the scatter plot with new hover data
                scatter_fig.update_traces(
                    hovertemplate=(
                        "Name: %{customdata[0]}<br>" +
                        "Author: %{customdata[1]}<br>" +
                        "Category: %{customdata[2]}<br>" +
                        "Cluster: %{color}<br>" +
                        "Cluster Name: %{customdata[3]}<br>" +
                        "Description: %{customdata[4]}<br>" +
                        "<extra></extra>"
                    ),
                    customdata=st.session_state.metadata[['Name', 'Author', 'Category', 'Cluster_Name', 'Cluster_Description']].values
                )
                
                # Update the plot in the container
                st.session_state.scatter_container.plotly_chart(scatter_fig, use_container_width=True)
                
                status_text.text("Cluster naming complete!")
            
        # Additional information
        st.subheader("Cluster Information")
        
        # Show cluster summary if available
        if st.session_state.cluster_summaries:
            for cluster in sorted(st.session_state.cluster_summaries.keys()):
                summary = st.session_state.cluster_summaries[cluster]
                with st.expander(f"Cluster {cluster}: {summary['name']}"):
                    st.write(f"**Description:** {summary['description']}")
                    st.write(f"**Number of documents:** {summary['size']}")
                    cluster_docs = st.session_state.metadata[st.session_state.metadata['Cluster'] == cluster]
                    st.write("**Documents:**")
                    st.dataframe(cluster_docs[['Name', 'Author', 'Category']])
        else:
            # Show simple cluster statistics
            st.bar_chart(st.session_state.metadata['Cluster'].value_counts())
        
        if st.checkbox("Show full metadata"):
            st.dataframe(st.session_state.metadata) 
