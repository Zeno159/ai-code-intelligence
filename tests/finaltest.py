from parser.repo_indexer import RepoIndexer
from embeddings.code_embedder import CodeEmbedder
from search.semantics import SematicSearch

indexer = RepoIndexer()
embedder = CodeEmbedder()
search = SematicSearch()
functions = indexer.index_repo("repos/sample_repo")
codes = [f["code"] for f in functions]
embeddings = embedder.embed_code(codes)
query = "function that prints stars"
query_embedding = embedder.embed_code(query)
result = search.search(query_embedding, embeddings, codes)
print("Best match:\n", result)