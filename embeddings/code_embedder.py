from sentence_transformers import SentenceTransformer

class CodeEmbedder:
    """
    Uses a pre-trained SentenceTransformer model to convert code snippets into vector embeddings.
    
    """
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    def embed_code(self,code_snippet):
        embedding = self.model.encode(code_snippet)
        return embedding