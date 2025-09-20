#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a visualização do grafo com pesos das arestas
"""

from generate_graph import generate_graph
from generate_visualization import generate_visualization

def main():
    print("Gerando grafo de cidades brasileiras...")
    grafo = generate_graph()
    
    print(f"Grafo criado com {grafo.number_of_nodes()} vértices e {grafo.number_of_edges()} arestas")
    
    # Mostra algumas informações do grafo
    print("\nArestas e seus pesos:")
    for u, v, data in grafo.edges(data=True):
        print(f"{u} ↔ {v}: {data['weight']} km")
    
    print("\nGerando visualização...")
    generate_visualization(grafo)
    
    print("Visualização salva! Abra o arquivo 'rotas_entregas.html' no navegador.")

if __name__ == "__main__":
    main()
