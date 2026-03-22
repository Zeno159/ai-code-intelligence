# AI Code Intelligence

An AI system that analyzes GitHub repositories using AST parsing, semantic search, and LLM-powered code explanation. Ask questions about any codebase in plain English and get accurate, context-aware answers.

## Overview

This project implements an end-to-end code intelligence pipeline combining:

- AST-based parsing to extract functions, classes, methods, and their relationships
- Semantic embeddings using SentenceTransformers for similarity search
- Dependency graph construction to understand how code components connect
- Context expansion that automatically pulls in related functions and callers
- LLM integration for developer-friendly code explanations using Google's Gemini API

## Features

✨ Key Capabilities:

- Parse Python repositories and extract rich metadata (parameters, calls, class membership)
- Automatically detect query intent — specific function, full class, or vague question
- Expand context beyond a single function by resolving dependencies and callers
- Semantic search to find the most relevant code for open-ended questions
- Gemini-powered explanations that reference the actual code, not just descriptions
- Supports both GitHub URLs (auto-cloned) and local folder paths
- Excludes sensitive files like `.env` and `secrets.py` from indexing

## Core Modules

### 1. `parser/function_extractor.py`
Parses Python files using the `ast` module to extract rich function and class metadata.

Key Class: `FunctionExtractor`
- Extracts function name, parameters, internal calls, class membership, and source code
- Methods:
  - `extract_functions_rich(file_path)` — returns full metadata per function including what it calls
  - `extract_classes_rich(file_path)` — returns a class with all its methods bundled together
  - `scan_repository_rich(repo_path)` — scans the entire repo, returns `(all_functions, all_classes)`

### 2. `parser/multi_language_parser.py`
Handles file-level dependency extraction across Python, JavaScript, and C++ files.

Key Class: `MultiLanguageParser`
- Resolves local `import` and `from` statements to actual file paths
- Methods:
  - `extract_dependencies(file_path, repo_path)` — returns list of dependent file paths
  - `scan_repository(repo_path)` — returns a dependency map for the entire repo

### 3. `parser/context_builder.py`
The core intelligence layer. Builds rich, structured context for the LLM by combining AST lookups, dependency expansion, and semantic search results.

Key Class: `ContextBuilder`
- Detects query intent by matching function/class names against the parsed codebase
- For named targets → direct AST lookup
- For vague queries → semantic search top-N results
- Expands context by resolving what the primary function calls and what calls it
- Methods:
  - `build_context(query, semantic_top_results)` — returns a context dict with `primary`, `dependencies`, `callers`, and a formatted `prompt_context` string ready for the LLM

### 4. `embeddings/code_embedder.py`
Converts code snippets into vector embeddings for semantic similarity search.

Key Class: `CodeEmbedder`
- Model: SentenceTransformers (`all-MiniLM-L6-v2`)
- Methods:
  - `embed_code(code_snippet)` — returns a vector embedding for a given code string

### 5. `search/semantics.py`
Performs cosine similarity search over embedded code snippets.

Key Class: `SemanticSearch`
- Methods:
  - `search(query_embedding, code_embeddings, code_snippets)` — returns single best match
  - `search_top_n(query_embedding, code_embeddings, code_snippets, top_n)` — returns top-N results as `(score, func_dict)` tuples

### 6. `agentwork.py`
Calls the Gemini API with the structured context built by `ContextBuilder`.

- Model: `gemini-2.0-flash`
- Loads API key from `.env` via `python-dotenv`
- Functions:
  - `explain_code(user_question, context)` — returns `question`, `intent`, `code_context`, and `explanation`

## Architecture Flow

```
GitHub URL or Local Folder Path
        ↓
[function_extractor.py] → AST parse all .py files → extract functions, classes, params, calls
        ↓
[code_embedder.py] → embed each function's source code into vectors
        ↓
User Query
        ↓
[context_builder.py] → detect intent (function / class / vague)
        ↓
        ├── Named function/class → AST direct lookup → expand dependencies + callers
        └── Vague query → semantic search top-N → expand dependencies + callers
        ↓
[agentwork.py] → format context → call Gemini API
        ↓
Output: Code snippet + developer-friendly explanation
```


## Example Queries

| Query | Intent Detected | What Happens |
|---|---|---|
| `"explain the Cart class"` | class | Fetches all methods of Cart + their dependencies |
| `"explain the login function"` | function | Fetches login + hash_password + generate_token |
| `"how does discounting work"` | vague | Semantic search returns top 5 relevant functions |
