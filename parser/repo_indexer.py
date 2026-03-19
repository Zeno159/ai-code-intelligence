import os
from parser.multi_language_parser import MultiLanguageParser

class RepoIndexer:
    def __init__(self):
        self.parser = MultiLanguageParser()

    def index_repo(self, repo_path):
        all_functions = []
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):  
                    file_path = os.path.join(root, file)

                    try:
                        functions = self.parser.extract_functions_with_code(file_path)

                        for func in functions:
                            all_functions.append({
                                "file": file,
                                "code": func
                            })

                    except Exception as e:
                        print(f"Error parsing {file_path}: {e}")

        return all_functions