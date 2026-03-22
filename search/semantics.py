import numpy as np
 
class SematicSearch:
    """
    This class implements a simple semantic search algorithm using cosine similarity.
    param query_embeddings: The embedding vector for the search query.
    param code_embeddings: A list of embedding vectors for the code snippets in the repository.
    param code_snippets: A list of code snippets corresponding to the embeddings.
    """
    def search(self,query_embeddings,code_embeddings,code_snippets):
        similarites=[]
        for emb in code_embeddings:
            sim = np.dot(query_embeddings,emb)/(np.linalg.norm(query_embeddings)*np.linalg.norm(emb))
            similarites.append(sim)
        best_index = np.argmax(similarites)
        return code_snippets[best_index]
    def search_top_n(self, query_embedding, code_embeddings, code_snippets, top_n=5):
        """
        Returns the top N most similar code snippets to the query based on cosine similarity.
        :param query_embedding: The embedding vector for the search query.
        :param code_embeddings: A list of embedding vectors for the code snippets in the repository.
        :param code_snippets: A list of code snippets corresponding to the embeddings.
        :param top_n: The number of top results to return.  
        :return: A list of tuples (similarity_score, code_snippet) sorted by similarity.
    """
        similarities = []
        for emb in code_embeddings:
            sim = np.dot(query_embedding, emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(emb)
            )
            similarities.append(sim)

        scored = sorted(
            zip(similarities, code_snippets),
            key=lambda x: x[0],
            reverse=True
        )
        return scored[:top_n]
