import ast
import os

class FunctionExtractor:
    def extract_functions(self, file_path):
        """
        Extracts function names from a Python file.
        :param file_path: Path to the Python file
        :return: A list of function names
        :rtype: list[str]
        """
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
        return functions


    def scan_repository(self, repo_path):
        """
        Scans a repository for Python files and extracts function names.
        :param repo_path: Path to the repository
        :return: A dictionary mapping file paths to lists of function names
        :rtype: dict[str, list[str]]
        """
        repo_functions = {}
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    functions = self.extract_functions(file_path)
                    repo_functions[file_path] = functions
        return repo_functions