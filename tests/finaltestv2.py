from parser.function_extractor import FunctionExtractor
from embeddings.code_embedder import CodeEmbedder
from search.semantics import SematicSearch
from parser.context_builder import ContextBuilder
from search.agentwork import explain_code

REPO_PATH = "./repos/sample_repo"
# idher funcrtions and classes dono chahiye, taaki context build kar sake
extractor = FunctionExtractor()
all_functions, all_classes = extractor.scan_repository_rich(REPO_PATH)
print(f"Indexed {len(all_functions)} functions across {len(all_classes)} classes")
#embedding all functions for semantic search
embedder = CodeEmbedder()
code_embeddings = [embedder.embed_code(f["code"]) for f in all_functions]

#build context for a query
builder = ContextBuilder(all_functions, all_classes)

#answer a query
query = "explain the login function?"

#using semantic search to get top relevant functions for vague queries
query_embedding = embedder.embed_code(query)
semantic_search = SematicSearch()
top_results = semantic_search.search_top_n(query_embedding, code_embeddings, all_functions, top_n=5)

context = builder.build_context(query, semantic_top_results=top_results)

print(f"\nDetected intent: {context['intent']}")
print(f"Primary snippets found: {len(context['primary'])}")
print(f"Dependencies found: {len(context['dependencies'])}")
print(f"Callers found: {len(context['callers'])}")

result = explain_code(user_question=query, context=context)

print("\n GEMINI EXPLANATION ")
print(result["explanation"])
