import networkx as nx
import os
class DependencyGraph:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_dependency(self, file, dependency):
        if file and dependency:  # guard against None/empty
            self.graph.add_edge(file, dependency)

    def build_graph(self, dependency_dict):
        """
        dependency_dict = {
            file1: [dep1, dep2],
            file2: [dep3]
        }
        """
        for file, deps in dependency_dict.items():
            self.graph.add_node(file)  # ensure isolated nodes appear too
            for dep in deps:
                self.add_dependency(file, dep)

        return self.graph

    def print_graph(self):
        print("=== Edges (file → dependency) ===")
        for edge in self.graph.edges():
            src = os.path.basename(edge[0])
            dep = os.path.basename(edge[1])
            print(f"{src}  →  {dep}")