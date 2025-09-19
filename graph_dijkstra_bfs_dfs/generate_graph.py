import networkx as nx
import random

# Garantir replicabilidade
random.seed(42)

def generate_graph():
    # Criar grafo simples
    G = nx.Graph()
    
    # Lista de cidades
    cidades = [
        "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba",
        "Porto Alegre", "Florianópolis", "Campinas", "Santos",
        "Brasília", "Goiânia", "Salvador", "Vitória"
    ]
    
    # Adiciona os vértices
    G.add_nodes_from(cidades)
    
    # Para garantir que o grafo seja conexo
    for i in range(len(cidades) - 1):
        peso = random.randint(100, 1000)  # distância fictícia em km
        G.add_edge(cidades[i], cidades[i+1], weight=peso)
    
    # Adiciona arestas extras, para ter multiplos caminhos possíveis entre cidades
    num_arestas_extras = 5
    while G.number_of_edges() < len(cidades) + num_arestas_extras:
        u, v = random.sample(cidades, 2)
        if not G.has_edge(u, v):  # só adiciona se ainda não existir
            peso = random.randint(100, 1000)
            G.add_edge(u, v, weight=peso)

    return G