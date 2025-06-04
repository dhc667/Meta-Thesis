from dataclasses import dataclass
from typing import Literal, List
import numpy as np

@dataclass
class VisualizationConfig:
    """Configuration parameters for the document visualization."""
    linkage_method: Literal["ward", "complete", "average", "single"] = "ward"
    dim_reduction: Literal["PCA", "TSNE"] = "PCA"
    cut_height: float | None = None  # If None, will be calculated from the data
    colors: List[str] | None = None  # If None, will use default colors
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
                "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
                "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5"
            ]
            
    def get_default_cut_height(self, linkage_matrix: np.ndarray) -> float:
        """Calculate the default cut height from the linkage matrix."""
        min_height = float(np.min(linkage_matrix[:, 2]))
        max_height = float(np.max(linkage_matrix[:, 2]))
        return min_height + (max_height - min_height) * 0.7 
