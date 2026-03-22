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

    def extract_functions_rich(self, file_path):
        """
        Extracts function definitions along with their code and metadata from a Python file.
        :param file_path: Path to the Python file
        :return: A list of function definitions with their code and metadata
        :rtype: list[dict]

        """
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        lines = source.splitlines()
        tree = ast.parse(source)
        results = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        results.append(self._extract_one(item, file_path, lines, class_name))

      
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not self._has_class_parent(tree, node):
                    results.append(self._extract_one(node, file_path, lines, class_name=None))

        return results

    def _extract_one(self, node, file_path, lines, class_name):
        
        """Build the rich dict for a single FunctionDef node."""
        params = [arg.arg for arg in node.args.args]
        calls = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)

        start = node.lineno - 1
        end = node.end_lineno  
        code = "\n".join(lines[start:end])

        return {
            "name": node.name,
            "class": class_name,
            "params": params,
            "calls": list(set(calls)),   
            "code": code,
            "file": file_path,
            "start_line": node.lineno,
            "end_line": node.end_lineno,
        }

    def _has_class_parent(self, tree, target_node):
        
        """Return True if target_node is a direct child of a ClassDef."""
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if item is target_node:
                        return True
        return False

    def extract_classes_rich(self, file_path):
        """
        Extracts class definitions along with their methods and metadata from a Python file.
        :param file_path: Path to the Python file
        :return: A list of class definitions
        :rtype: list[dict]
        """
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        lines = source.splitlines()
        tree = ast.parse(source)
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append(self._extract_one(item, file_path, lines, node.name))
                classes.append({
                    "name": node.name,
                    "methods": methods,
                    "file": file_path,
                })

        return classes

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
    
    def scan_repository_rich(self, repo_path):
        """
        Scans the entire repo and returns a flat list of rich function dicts
        plus a separate list of class dicts.
        Returns:
            functions: list of rich function dicts (all functions + methods)
            classes: list of class dicts (each with its methods embedded)
        """
        all_functions = []
        all_classes = []

        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        all_functions.extend(self.extract_functions_rich(file_path))
                        all_classes.extend(self.extract_classes_rich(file_path))
                    except Exception as e:
                        print(f"[FunctionExtractor] Skipping {file_path}: {e}")

        return all_functions, all_classes
