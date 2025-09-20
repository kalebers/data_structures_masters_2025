import networkx as nx
import random
from pyvis.network import Network

from generate_graph import generate_graph
from generate_visualization import generate_visualization


# Garantir replicabilidade
random.seed(42)

# Gera grafo inicial
G = generate_graph()

# Gera visualização do grafo
generate_visualization(G)

# Chamar algoritmos aqui