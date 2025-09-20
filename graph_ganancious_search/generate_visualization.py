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
        "smooth": false,
        "font": {
          "size": 12,
          "color": "red",
          "strokeWidth": 2,
          "strokeColor": "white"
        }
      },
      "nodes": {
        "size": 20,
        "font": {
          "size": 14,
          "color": "black"
        }
      }
    }
    """)
    
    # Converter o grafo NetworkX para Pyvis
    for node in graph.nodes():
        net.add_node(node, label=node)
    
    for u, v, data in graph.edges(data=True):
        weight = data['weight']
        net.add_edge(u, v, 
                    label=str(weight),  # Mostra o peso como label na aresta
                    value=weight/10,    # Ajusta a espessura da linha
                    title=f"Distância: {weight} km",  # Tooltip ao passar o mouse
                    font={'size': 12, 'color': 'red', 'strokeWidth': 2, 'strokeColor': 'white'})
    
    # Salvar em HTML
    net.show("rotas_entregas.html", notebook=False)
    print("Grafo salvo como 'rotas_entregas.html'. Abra no navegador para visualizar.")

