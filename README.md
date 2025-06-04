# Meta-Thesis Document Visualization System

This project provides an interactive document visualization system that helps analyze and explore collections of academic papers through clustering and topic analysis.

## Features

- Document embedding and clustering
- Interactive visualization with Streamlit
- Hierarchical clustering with adjustable parameters
- Automatic topic summarization for clusters
- Real-time cluster exploration and analysis
- Support for multiple embedding types
- Beautiful interactive visualizations using Plotly and Matplotlib

## Project Structure

The project is organized into several key modules:

- `presenter/`: Contains the visualization and presentation logic
  - Interactive Streamlit interface
  - Document clustering and visualization
  - Topic summarization
- `dataset_builder/`: Handles document processing and embedding
  - Document parsing and storage
  - Embedding generation
  - Repository management

## Prerequisites

- Python 3.8+
- Make
- pip

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd Meta-Thesis
```

2. Install dependencies:
```bash
make install-dependencies
```

## Usage

The project provides two main commands through the Makefile:

### 1. Index Documents

To process and index your documents:

```bash
make index
```

This command will:
- Process your input documents
- Generate embeddings
- Store them in the repository

### 2. Launch Visualization Interface

To start the interactive visualization:

```bash
make present
```

This will launch the Streamlit interface where you can:
- View document clusters in an interactive scatter plot
- Explore the hierarchical structure through dendrograms
- Adjust clustering parameters in real-time
- Generate automatic topic summaries for clusters
- View detailed document metadata

## Interactive Features

The visualization interface provides several interactive features:

1. **Clustering Parameters**
   - Adjust linkage method (ward, complete, average, single)
   - Modify cut height to control number of clusters
   - Choose dimensionality reduction technique (PCA or t-SNE)

2. **Visualizations**
   - Interactive dendrogram showing hierarchical structure
   - 2D scatter plot of document clusters
   - Hover information for detailed document metadata

3. **Topic Analysis**
   - Automatic cluster naming based on document content
   - Topic summaries for each cluster
   - Document listings within clusters
