import networkx as nx
import random
import time
import statistics

# Importar as implementações dos algoritmos dos arquivos separados
from dijkstra_metrics import dijkstra
from bfs_metrics import bfs
from dfs_metrics import dfs

from generate_graph import generate_graph
from generate_visualization import generate_visualization


# Garantir replicabilidade
random.seed(42)

# Gera grafo inicial
G = generate_graph()

# Gera visualização do grafo (opcional)
# generate_visualization(G)

# Casos de teste
test_cases = [
    ("São Paulo", "Florianópolis"),
    ("Rio de Janeiro", "Goiânia"),
    ("Belo Horizonte", "Vitória"),
    ("Curitiba", "Salvador"),
    ("Campinas", "Brasília")
]

# Função para executar e coletar métricas
def run_and_collect_metrics(algorithm_func, graph, start, end, num_runs=5):
    all_metrics = {
        'paths': [],
        'costs': [],
        'expanded_nodes': [],
        'times': []
    }
    
    for _ in range(num_runs):
        start_time = time.time()
        path, cost, expanded_nodes = algorithm_func(graph, start, end)
        end_time = time.time()
        
        all_metrics['paths'].append(path)
        all_metrics['costs'].append(cost)
        all_metrics['expanded_nodes'].append(expanded_nodes)
        all_metrics['times'].append(end_time - start_time)
        
    return all_metrics

def save_results_to_file(results, filename="analise_desempenho_grafos.txt"):
    with open(filename, 'w') as f:
        f.write("Análise Comparativa de Algoritmos de Busca em Grafos\n")
        f.write("=" * 60 + "\n\n")

        for (start_node, end_node), algos in results.items():
            f.write(f"--- Comparando de {start_node} para {end_node} ---\n")
            for algo_name, metrics in algos.items():
                
                if metrics['costs'][0] == float('inf'):
                    f.write(f"Algoritmo {algo_name}:\n")
                    f.write("  Não encontrou um caminho.\n")
                    f.write("-" * 20 + "\n")
                    continue

                avg_cost = statistics.mean(metrics['costs'])
                avg_expanded_nodes = statistics.mean(metrics['expanded_nodes'])
                avg_time = statistics.mean(metrics['times'])
                
                std_dev_cost = statistics.stdev(metrics['costs']) if len(metrics['costs']) > 1 else 0
                std_dev_expanded_nodes = statistics.stdev(metrics['expanded_nodes']) if len(metrics['expanded_nodes']) > 1 else 0
                std_dev_time = statistics.stdev(metrics['times']) if len(metrics['times']) > 1 else 0

                f.write(f"Algoritmo {algo_name}:\n")
                f.write(f"  Caminho Encontrado: {metrics['paths'][0]}\n")
                f.write(f"  Custo Médio: {avg_cost:.2f} | Desvio Padrão: {std_dev_cost:.2f}\n")
                f.write(f"  Nós Expandidos Médio: {avg_expanded_nodes:.2f} | Desvio Padrão: {std_dev_expanded_nodes:.2f}\n")
                f.write(f"  Tempo Médio: {avg_time:.6f}s | Desvio Padrão: {std_dev_time:.6f}s\n")
                f.write("-" * 20 + "\n")
            f.write("\n")
    print(f"Resultados salvos em '{filename}'.")


# ==========================================================
# Início do programa principal
# ==========================================================
# Comparação e Análise
results = {}
for start_node, end_node in test_cases:
    print(f"--- Comparando de {start_node} para {end_node} ---")
    
    results[(start_node, end_node)] = {
        'Dijkstra': run_and_collect_metrics(dijkstra, G, start_node, end_node),
        'DFS': run_and_collect_metrics(dfs, G, start_node, end_node),
        'BFS': run_and_collect_metrics(bfs, G, start_node, end_node)
    }

    dijkstra_metrics = results[(start_node, end_node)]['Dijkstra']
    dfs_metrics = results[(start_node, end_node)]['DFS']
    bfs_metrics = results[(start_node, end_node)]['BFS']
    
    # Exemplo de impressão de resultados no console
    print(f"Algoritmo Dijkstra: Custo Médio: {sum(dijkstra_metrics['costs']) / len(dijkstra_metrics['costs']):.2f} | Nós Expandidos Médio: {sum(dijkstra_metrics['expanded_nodes']) / len(dijkstra_metrics['expanded_nodes']):.2f} | Tempo Médio: {sum(dijkstra_metrics['times']) / len(dijkstra_metrics['times']):.6f}s")
    
    print(f"Algoritmo DFS: Custo Médio: {sum(dfs_metrics['costs']) / len(dfs_metrics['costs']):.2f} | Nós Expandidos Médio: {sum(dfs_metrics['expanded_nodes']) / len(dfs_metrics['expanded_nodes']):.2f} | Tempo Médio: {sum(dfs_metrics['times']) / len(dfs_metrics['times']):.6f}s")
    
    print(f"Algoritmo BFS: Custo Médio: {sum(bfs_metrics['costs']) / len(bfs_metrics['costs']):.2f} | Nós Expandidos Médio: {sum(bfs_metrics['expanded_nodes']) / len(bfs_metrics['expanded_nodes']):.2f} | Tempo Médio: {sum(bfs_metrics['times']) / len(bfs_metrics['times']):.6f}s")
    print("-" * 30)

# Salva os resultados em um arquivo de texto
save_results_to_file(results)