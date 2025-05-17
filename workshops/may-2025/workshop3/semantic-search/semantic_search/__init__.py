# Package initialization file
__version__ = "0.1.0"

from semantic_search.search import SemanticSearch
from semantic_search.embedding import EmbeddingGenerator

__all__ = ['SemanticSearch', 'EmbeddingGenerator']