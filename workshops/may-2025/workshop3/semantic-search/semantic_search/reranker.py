# Re-ranking module for semantic search application
from typing import List, Dict, Any
import numpy as np
from statistics import mean

class ReRanker:
    """Class for re-ranking search results using various techniques."""
    
    def __init__(self):
        """Initialize the re-ranker."""
        pass
    
    def bm25_rerank(self, query: str, results: Dict[str, Any], k1: float = 1.5, b: float = 0.75) -> Dict[str, Any]:
        """
        Re-rank results using BM25 scoring (a classic lexical ranking algorithm).
        
        Args:
            query: The search query
            results: The original search results
            k1: BM25 parameter for term frequency saturation
            b: BM25 parameter for document length normalization
        
        Returns:
            Re-ranked search results
        """
        if not results or 'documents' not in results or not results['documents'][0]:
            return results
        
        # Extract documents and their original scores
        documents = results['documents'][0]
        original_scores = [1 - dist for dist in results['distances'][0]]  # Convert distances to scores
        metadatas = results['metadatas'][0]
        
        # Process the query (simple tokenization)
        query_terms = query.lower().split()
        
        # Calculate document lengths and average document length
        doc_lengths = [len(doc.split()) for doc in documents]
        avg_doc_length = mean(doc_lengths)
        
        # Calculate corpus-wide term frequencies (simple approach)
        term_doc_counts = {}
        for term in query_terms:
            term_doc_counts[term] = sum(1 for doc in documents if term.lower() in doc.lower())
        
        # Calculate BM25 scores
        bm25_scores = []
        
        for i, doc in enumerate(documents):
            doc_terms = doc.lower().split()
            doc_length = doc_lengths[i]
            
            score = 0
            for term in query_terms:
                if term_doc_counts[term] == 0:
                    continue
                    
                # Calculate term frequency in this document
                tf = doc.lower().count(term.lower())
                
                # Inverse document frequency
                idf = np.log((len(documents) - term_doc_counts[term] + 0.5) / 
                            (term_doc_counts[term] + 0.5) + 1)
                
                # BM25 term score
                term_score = idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_length / avg_doc_length))
                
                score += term_score
                
            bm25_scores.append(score)
        
        # Combine BM25 scores with original semantic scores (50/50 weight)
        # Normalize scores first
        if max(bm25_scores) > 0:
            bm25_scores = [score / max(bm25_scores) for score in bm25_scores]
        
        combined_scores = [0.5 * bm25 + 0.5 * semantic 
                          for bm25, semantic in zip(bm25_scores, original_scores)]
        
        # Re-sort the results based on the combined scores
        sorted_indices = sorted(range(len(combined_scores)), key=lambda i: combined_scores[i], reverse=True)
        
        # Create re-ranked results
        reranked_results = {
            'documents': [[documents[i] for i in sorted_indices]],
            'metadatas': [[metadatas[i] for i in sorted_indices]],
            'distances': [[1 - combined_scores[i] for i in sorted_indices]],  # Convert scores back to distances
        }
        
        return reranked_results
    
    def diversity_rerank(self, results: Dict[str, Any], diversity_factor: float = 0.5) -> Dict[str, Any]:
        """
        Re-rank results to increase diversity using Maximal Marginal Relevance (MMR).
        
        Args:
            results: The original search results
            diversity_factor: How much to prioritize diversity (0-1, higher means more diverse)
        
        Returns:
            Re-ranked search results with increased diversity
        """
        if not results or 'documents' not in results or not results['documents'][0]:
            return results
        
        # Extract documents and their original scores
        documents = results['documents'][0]
        original_scores = [1 - dist for dist in results['distances'][0]]  # Convert distances to scores
        metadatas = results['metadatas'][0]
        
        # Simple TF-IDF vectorization for documents
        # In a real application, you would use embeddings directly if available
        
        # Create a vocabulary
        all_words = set()
        doc_words = []
        
        for doc in documents:
            words = set(doc.lower().split())
            doc_words.append(words)
            all_words.update(words)
        
        vocabulary = list(all_words)
        
        # Create document vectors
        doc_vectors = []
        for words in doc_words:
            vector = [1 if word in words else 0 for word in vocabulary]
            # Normalize
            magnitude = np.sqrt(sum(v * v for v in vector))
            if magnitude > 0:
                vector = [v / magnitude for v in vector]
            doc_vectors.append(vector)
        
        # MMR algorithm
        selected_indices = []
        remaining_indices = list(range(len(documents)))
        
        # Select the highest scoring document first
        best_idx = max(remaining_indices, key=lambda i: original_scores[i])
        selected_indices.append(best_idx)
        remaining_indices.remove(best_idx)
        
        # Select the rest using MMR
        while remaining_indices:
            best_score = -1
            best_idx = -1
            
            for i in remaining_indices:
                # Relevance score (from original ranking)
                relevance = original_scores[i]
                
                # Diversity score (maximum similarity to any selected document)
                max_similarity = max(
                    [self._cosine_similarity(doc_vectors[i], doc_vectors[j]) 
                     for j in selected_indices],
                    default=0
                )
                
                # MMR score
                mmr_score = (1 - diversity_factor) * relevance - diversity_factor * max_similarity
                
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = i
            
            selected_indices.append(best_idx)
            remaining_indices.remove(best_idx)
        
        # Create re-ranked results
        reranked_results = {
            'documents': [[documents[i] for i in selected_indices]],
            'metadatas': [[metadatas[i] for i in selected_indices]],
            'distances': [[1 - original_scores[i] for i in selected_indices]],  # Convert scores back to distances
        }
        
        return reranked_results
    
    def recency_rerank(self, results: Dict[str, Any], recency_weight: float = 0.3) -> Dict[str, Any]:
        """
        Re-rank results to boost more recent documents.
        Requires 'date' or 'timestamp' in document metadata.
        
        Args:
            results: The original search results
            recency_weight: How much to prioritize recency (0-1)
        
        Returns:
            Re-ranked search results with recency boost
        """
        if not results or 'documents' not in results or not results['documents'][0]:
            return results
        
        # Extract documents and their original scores
        documents = results['documents'][0]
        original_scores = [1 - dist for dist in results['distances'][0]]  # Convert distances to scores
        metadatas = results['metadatas'][0]
        
        # Check if we have date information
        has_date = all('date' in meta or 'timestamp' in meta for meta in metadatas)
        if not has_date:
            print("Warning: Cannot perform recency re-ranking as documents lack date metadata")
            return results
        
        # Extract dates (using 'date' or 'timestamp' field)
        dates = []
        for meta in metadatas:
            if 'date' in meta:
                dates.append(meta['date'])
            elif 'timestamp' in meta:
                dates.append(meta['timestamp'])
            else:
                dates.append(None)
        
        # Convert to numeric values (assuming ISO format dates or Unix timestamps)
        # This is a simplified version - in a real application, use proper date parsing
        try:
            numeric_dates = [float(date) if date else 0 for date in dates]
            
            # Normalize dates to 0-1 range
            if max(numeric_dates) > min(numeric_dates):
                normalized_dates = [(d - min(numeric_dates)) / (max(numeric_dates) - min(numeric_dates)) 
                                  for d in numeric_dates]
            else:
                normalized_dates = [1.0 for _ in numeric_dates]
                
        except (ValueError, TypeError):
            print("Warning: Date conversion failed, skipping recency re-ranking")
            return results
        
        # Combine original scores with recency scores
        combined_scores = [(1 - recency_weight) * score + recency_weight * recency 
                          for score, recency in zip(original_scores, normalized_dates)]
        
        # Re-sort the results based on the combined scores
        sorted_indices = sorted(range(len(combined_scores)), key=lambda i: combined_scores[i], reverse=True)
        
        # Create re-ranked results
        reranked_results = {
            'documents': [[documents[i] for i in sorted_indices]],
            'metadatas': [[metadatas[i] for i in sorted_indices]],
            'distances': [[1 - combined_scores[i] for i in sorted_indices]],  # Convert scores back to distances
        }
        
        return reranked_results
    
    def personalized_rerank(self, results: Dict[str, Any], user_profile: Dict[str, float]) -> Dict[str, Any]:
        """
        Re-rank results based on user preferences.
        
        Args:
            results: The original search results
            user_profile: Dictionary of user preferences (keywords -> weights)
        
        Returns:
            Re-ranked search results with personalization
        """
        if not results or 'documents' not in results or not results['documents'][0]:
            return results
        
        if not user_profile:
            return results
        
        # Extract documents and their original scores
        documents = results['documents'][0]
        original_scores = [1 - dist for dist in results['distances'][0]]  # Convert distances to scores
        metadatas = results['metadatas'][0]
        
        # Calculate personalization scores
        personalization_scores = []
        
        for doc in documents:
            doc_lower = doc.lower()
            
            # Calculate a score based on presence of profile keywords
            score = 0
            for keyword, weight in user_profile.items():
                if keyword.lower() in doc_lower:
                    # Count occurrences and apply weight
                    count = doc_lower.count(keyword.lower())
                    score += count * weight
            
            personalization_scores.append(score)
        
        # Normalize personalization scores
        if max(personalization_scores) > 0:
            personalization_scores = [score / max(personalization_scores) for score in personalization_scores]
        
        # Combine scores (70% original, 30% personalization)
        combined_scores = [0.7 * orig + 0.3 * pers 
                          for orig, pers in zip(original_scores, personalization_scores)]
        
        # Re-sort the results based on the combined scores
        sorted_indices = sorted(range(len(combined_scores)), key=lambda i: combined_scores[i], reverse=True)
        
        # Create re-ranked results
        reranked_results = {
            'documents': [[documents[i] for i in sorted_indices]],
            'metadatas': [[metadatas[i] for i in sorted_indices]],
            'distances': [[1 - combined_scores[i] for i in sorted_indices]],  # Convert scores back to distances
        }
        
        return reranked_results
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = np.sqrt(sum(a * a for a in vec1))
        magnitude2 = np.sqrt(sum(b * b for b in vec2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
            
        return dot_product / (magnitude1 * magnitude2)