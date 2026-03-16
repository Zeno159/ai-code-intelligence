import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parser.multi_language_parser import MultiLanguageParser
from parser.dependency_graph import DependencyGraph

parser = MultiLanguageParser()


repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "repos"))

deps = parser.scan_repository(repo_path)
graph_builder = DependencyGraph()
graph = graph_builder.build_graph(deps)
graph_builder.print_graph()