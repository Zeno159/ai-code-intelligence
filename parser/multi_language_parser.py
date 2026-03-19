import os

class MultiLanguageParser:
    def __init__(self):
        self.supported = {".py", ".js", ".cpp"}

    def extract_dependencies(self, file_path, repo_path):
        """
        Extracts dependencies from a file based on its extension.
        :param file_path: Path to the file being scanned
        :param repo_path: Path to the repository for resolving local imports
        :return: A list of file paths that are dependencies of the given file
        :rtype: list[str]
        
        """
        dependencies = []
        file_dir = os.path.dirname(file_path)  # directory of the file being scanned

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            module = None

            if line.startswith("import "):
                module = line.split()[1].split(".")[0]
            elif line.startswith("from "):
                module = line.split()[1].split(".")[0]

            if module:
                candidate = os.path.join(file_dir, module + ".py")
                if os.path.exists(candidate):
                    dependencies.append(os.path.abspath(candidate))
                else:
              
                    candidate = os.path.join(repo_path, module + ".py")
                    if os.path.exists(candidate):
                        dependencies.append(os.path.abspath(candidate))

        return dependencies

    def scan_repository(self, repo_path):
        """
        Scans a repository for supported files and extracts their dependencies.
        :param repo_path: Path to the repository
        :return: A dictionary mapping file paths to their dependencies
        :rtype: dict[str, list[str]]
        """
        repo_path = os.path.abspath(repo_path) 
        dependency_map = {}

        for root, dirs, files in os.walk(repo_path):
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext in self.supported:
                    file_path = os.path.join(root, file)
                    deps = self.extract_dependencies(file_path, repo_path)
                    dependency_map[os.path.abspath(file_path)] = deps

        return dependency_map
    
    def extract_functions_with_code(self, file_path):
        
        """
        Extracts function definitions along with their code from a Python file.
        :param file_path: Path to the Python file
        :return: A list of function definitions with their code
        :rtype: list[str]
        """
 
        functions = []

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        inside_function = False
        func_code = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("def "):
                if inside_function:
                    functions.append("".join(func_code))
                inside_function = True
                func_code = [line]
            elif inside_function:
                func_code.append(line)
        if inside_function:
            functions.append("".join(func_code))

        return functions