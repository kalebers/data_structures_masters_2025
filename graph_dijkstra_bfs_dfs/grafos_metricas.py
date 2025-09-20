import networkx as nx
import random
import time
import statistics
import matplotlib.pyplot as plt

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

def save_big_o_analysis(file):
    """Adiciona a análise da Notação Big-O ao arquivo de resultados."""
    file.write("=" * 60 + "\n")
    file.write("Análise da Complexidade de Algoritmos (Notação Big-O)\n")
    file.write("=" * 60 + "\n\n")
    file.write("A notacao Big-O e usada para descrever o desempenho ou complexidade de um algoritmo. Ela mede o tempo de execucao no pior cenario, ou a quantidade de espaco de memoria usada por um algoritmo, a medida que o tamanho dos dados de entrada cresce.\n\n")
    
    file.write("1.  **Algoritmo de Dijkstra:**\n")
    file.write("    A complexidade de tempo de Dijkstra em um grafo com V vertices e E arestas, usando um heap de prioridade, e O(E log V).\n")
    file.write("    Isso ocorre porque cada aresta e examinada uma vez e cada operacao de heap (insercao e extracao) leva tempo O(log V).\n\n")

    file.write("2.  **Busca em Largura (BFS):**\n")
    file.write("    A complexidade de tempo do BFS e O(V+E).\n")
    file.write("    No pior cenario, o algoritmo visita cada vertice e cada aresta exatamente uma vez, tornando sua complexidade linear ao tamanho do grafo.\n\n")

    file.write("3.  **Busca em Profundidade (DFS):**\n")
    file.write("    Assim como o BFS, a complexidade de tempo do DFS e O(V+E).\n")
    file.write("    Ele explora o grafo em profundidade, mas cada vertice e aresta e visitado uma unica vez, resultando em uma complexidade linear.\n\n")

    file.write("4.  **Comparacao:**\n")
    file.write("    - Dijkstra e ideal para encontrar o caminho mais curto em grafos com pesos positivos. Sua complexidade e sensivel ao numero de arestas.\n")
    file.write("    - DFS e BFS sao mais simples e garantem encontrar um caminho. O BFS encontra o caminho mais curto em termos de numero de arestas (sem pesos), enquanto o DFS e eficiente em termos de memoria.\n")

def create_plots(results):
    """Cria e salva gráficos comparativos das métricas."""
    
    # Extrair os nomes dos algoritmos
    algorithms = list(results[list(results.keys())[0]].keys())
    
    # Preparar dados para os plots
    plot_data = {
        'Custo Medio': {},
        'Nos Expandidos Medio': {},
        'Tempo Medio': {}
    }
    
    for metric_name in plot_data.keys():
        plot_data[metric_name] = {algo: [] for algo in algorithms}
    
    case_labels = []
    
    for (start_node, end_node), algos in results.items():
        case_labels.append(f"{start_node} para {end_node}")
        for algo_name, metrics in algos.items():
            if metrics['costs']:
                plot_data['Custo Medio'][algo_name].append(statistics.mean(metrics['costs']))
                plot_data['Nos Expandidos Medio'][algo_name].append(statistics.mean(metrics['expanded_nodes']))
                plot_data['Tempo Medio'][algo_name].append(statistics.mean(metrics['times']) * 1000) # Converte para milissegundos
            else:
                # Caso o algoritmo não encontre um caminho
                plot_data['Custo Medio'][algo_name].append(0)
                plot_data['Nos Expandidos Medio'][algo_name].append(0)
                plot_data['Tempo Medio'][algo_name].append(0)

    # Plotar os gráficos
    x = range(len(case_labels))
    width = 0.25  # Largura das barras

    for i, (metric_name, metric_data) in enumerate(plot_data.items()):
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for j, (algo_name, values) in enumerate(metric_data.items()):
            offset = (j - len(algorithms) / 2 + 0.5) * width
            ax.bar([pos + offset for pos in x], values, width, label=algo_name)
        
        ax.set_ylabel(metric_name)
        ax.set_title(f"Comparação de {metric_name} por Caso de Teste")
        ax.set_xticks(x)
        ax.set_xticklabels(case_labels, rotation=45, ha="right")
        ax.legend()
        plt.tight_layout()
        plt.savefig(f"{metric_name.replace(' ', '_')}_comparativo.png")
        plt.show()

def save_results_to_file(results, filename="analise_desempenho_grafos.txt"):
    # Adicionando a codificação UTF-8 para evitar problemas de caracteres
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Análise Comparativa de Algoritmos de Busca em Grafos\n")
        f.write("=" * 60 + "\n\n")

        for (start_node, end_node), algos in results.items():
            f.write(f"--- Comparando de {start_node} para {end_node} ---\n")
            for algo_name, metrics in algos.items():
                
                if not metrics['paths'] or metrics['costs'][0] == float('inf'):
                    f.write(f"Algoritmo {algo_name}:\n")
                    f.write("  Nao encontrou um caminho.\n")
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
                f.write(f"  Custo Medio: {avg_cost:.2f} | Desvio Padrao: {std_dev_cost:.2f}\n")
                f.write(f"  Nos Expandidos Medio: {avg_expanded_nodes:.2f} | Desvio Padrao: {std_dev_expanded_nodes:.2f}\n")
                f.write(f"  Tempo Medio: {avg_time:.6f}s | Desvio Padrao: {std_dev_time:.6f}s\n")
                f.write("-" * 20 + "\n")
            f.write("\n")
        
        save_big_o_analysis(f)

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
    print(f"Algoritmo Dijkstra: Custo Medio: {sum(dijkstra_metrics['costs']) / len(dijkstra_metrics['costs']):.2f} | Nos Expandidos Medio: {sum(dijkstra_metrics['expanded_nodes']) / len(dijkstra_metrics['expanded_nodes']):.2f} | Tempo Medio: {sum(dijkstra_metrics['times']) / len(dijkstra_metrics['times']):.6f}s")
    
    print(f"Algoritmo DFS: Custo Medio: {sum(dfs_metrics['costs']) / len(dfs_metrics['costs']):.2f} | Nos Expandidos Medio: {sum(dfs_metrics['expanded_nodes']) / len(dfs_metrics['expanded_nodes']):.2f} | Tempo Medio: {sum(dfs_metrics['times']) / len(dfs_metrics['times']):.6f}s")
    
    print(f"Algoritmo BFS: Custo Medio: {sum(bfs_metrics['costs']) / len(bfs_metrics['costs']):.2f} | Nos Expandidos Medio: {sum(bfs_metrics['expanded_nodes']) / len(bfs_metrics['expanded_nodes']):.2f} | Tempo Medio: {sum(bfs_metrics['times']) / len(bfs_metrics['times']):.6f}s")
    print("-" * 30)

# Salva os resultados em um arquivo de texto
save_results_to_file(results)

# Cria e salva os plots
create_plots(results)