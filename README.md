##Introduction
AI Code Intelligence is a system that analyzes GitHub repositories using a combination of AST parsing, graph-based analysis, and AI-powered review agents. The goal is to understand code structure deeply and generate meaningful insights about how a codebase works.

##Project Structure

parser/
This folder handles parsing of source code using Abstract Syntax Trees (AST). It extracts important elements like functions, classes, and their structure, which becomes the foundation for further analysis.

embeddings/
Responsible for semantic understanding of code. It converts code into vector representations so that similar pieces of code can be searched or compared efficiently.

search/
This folder contains the semantic.py file which generate a list of code snippet corresponding to the embeddings, which in this case is user query 


tests/
Includes test cases to verify that different parts of the system are working correctly.

#How It Works

The system starts by taking a repository as input. The parser reads the code files and converts them into structured representations using ASTs. Once the structure is extracted, the graph module builds connections between different components of the code, such as which functions call each other.

After that, the embeddings module processes the code to capture its semantic meaning, making it easier to search and compare different parts of the repository.

Finally, the agents use all this information — structure, relationships, and semantics — to generate insights about the code. This can include understanding the flow of the program, identifying improvements, or summarizing parts of the repository.
