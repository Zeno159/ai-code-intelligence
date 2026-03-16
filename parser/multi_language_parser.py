import os

class MultiLanguageParser:
    def __init__(self):
        self.supported = {".py", ".js", ".cpp"}

    def extract_dependencies(self, file_path, repo_path):
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
            # check relative to the file's own folder first
                candidate = os.path.join(file_dir, module + ".py")
                if os.path.exists(candidate):
                    dependencies.append(os.path.abspath(candidate))
                else:
              
                    candidate = os.path.join(repo_path, module + ".py")
                    if os.path.exists(candidate):
                        dependencies.append(os.path.abspath(candidate))

        return dependencies

    def scan_repository(self, repo_path):
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