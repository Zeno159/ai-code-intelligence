import ast
import os

class Function_extractor:
    def extract_function(self,file_path):
        """
           Docstring for extract_function
           
        :param self: the instance of the class
        :param file_path: a string representing the path to the file to be scanned
        :return: a list of function names defined in the file
        :rtype: list[str]
        """
        with open(file_path,"r",encoding = "utf-8") as f:
            tree = ast.parse(f.read())
        functions=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.FunctionDef):
                functions.append(node.name)
        return functions

    def scan_repository(self,repo_path):
        """
        Docstring for scan_repository
        :param self: the instance of the class
        :param repo_path: a string representing the path to the repository to be scanned
        :return: a dictionary mapping file paths to lists of function names
        :rtype: dict[str, list[str]]
        """
        repo_function = []

        for root,dirs,files in os.walk(repo_path):
            for file in files:
                if(files.endswith(".py")):
                    file_path = os.path.join(root,file)
                    functions = self.extract_function(file_path)
                    repo_function[file_path]= functions
        return repo_function