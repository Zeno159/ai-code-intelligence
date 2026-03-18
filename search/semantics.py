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