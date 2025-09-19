import networkx as nx
import random
from pyvis.network import Network

def generate_visualization(graph):
    # Visualização com Pyvis
    net = Network(notebook=False, height="1080px", width="100%", bgcolor="#ffffff", font_color="black")
    
    # Altera algumas configurações pra ficar mais visualmente agradável
    net.set_options("""
    var options = {
      "physics": {
        "enabled": true,
        "stabilization": {
          "enabled": true
        },
        "repulsion": {
          "nodeDistance": 300 
        }
      },
      "edges": {
        "smooth": false
      },
      "nodes": {
        "size": 20 
      }
    }
    """)
    
    # Converter o grafo NetworkX para Pyvis
    for node in graph.nodes():
        net.add_node(node, label=node)
    
    for u, v, data in graph.edges(data=True):
        net.add_edge(u, v, value=data['weight'], title=f"Distância: {data['weight']} km")
    
    # Salvar em HTML
    net.show("rotas_entregas.html", notebook=False)
    print("Grafo salvo como 'rotas_entregas.html'. Abra no navegador para visualizar.")

