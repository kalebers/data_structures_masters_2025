# Main code to run for BST vs AVL comparison. It calls the relatorio.py module to generate the report.
# ------------------------

import sys
import time
import tracemalloc
import random
import matplotlib.pyplot as plt
from relatorio import generate_html_report 

# Aumenta o limite de recursão para árvores profundas (necessário para a BST não balanceada)
sys.setrecursionlimit(200000)

## Classe Node
class Node:
    """Representa um nó na árvore de busca, com seus dados e ponteiros."""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


# 1. Árvore de Busca Binária (BST)
class BinaryTree:

    def __init__(self):
        self.root = None
    
    def insert(self, data):
        self.root = self._insert_node(self.root, data)
    
    def _insert_node(self, node, data):
        if node is None:
            return Node(data)
        
        if data < node.data:
            node.left = self._insert_node(node.left, data)
        elif data > node.data:
            node.right = self._insert_node(node.right, data)
        
        return node
    
    def search(self, data):
        return self._search_node(self.root, data)
    
    def _search_node(self, node, data):
        if node is None or node.data == data:
            return node
        
        if data < node.data:
            return self._search_node(node.left, data)
        else:
            return self._search_node(node.right, data)

# 2. Árvore de Busca Balanceada AVL
class AVLTree:

    def __init__(self):
        self.root = None
        
    def _get_height(self, node):
        return node.height if node else 0
    
    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
        
    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        
        y.right = z
        z.left = T3
        
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y
        
    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        
        y.left = z
        z.right = T2
        
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y

    def insert(self, data):
        self.root = self._insert_node(self.root, data)
        
    def _insert_node(self, node, data):
        if not node:
            return Node(data)
        
        if data < node.data:
            node.left = self._insert_node(node.left, data)
        else: # data >= node.data para evitar duplicação
            node.right = self._insert_node(node.right, data)
        
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        
        balance = self._get_balance(node)
        
        # Casos de Rotação
        # Left Left
        if balance > 1 and data < node.left.data:
            return self._right_rotate(node)
        
        # Right Right
        if balance < -1 and data > node.right.data:
            return self._left_rotate(node)
        
        # Left Right
        if balance > 1 and data > node.left.data:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
            
        # Right Left
        if balance < -1 and data < node.right.data:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
            
        return node
        
    def search(self, data):
        return self._search_node(self.root, data)
    
    def _search_node(self, node, data):
        if node is None or node.data == data:
            return node
        
        if data < node.data:
            return self._search_node(node.left, data)
        else:
            return self._search_node(node.right, data)

## Testes e Geração de Métricas
def run_tests(tree, data_size, num_runs=5):

    print(f"\nTeste com {type(tree).__name__} e N = {data_size} registros...")
    
    insert_times = []
    search_times = []
    insert_memories = []
    search_memories = []
    
    # Coletar dados sintéticos
    random.seed(42)
    data_to_insert = [random.randint(100000000, 999999999) for _ in range(data_size)]
    data_to_search = data_to_insert[:]
    
    for i in range(num_runs):
        print(f"   > Rodada {i+1} de {num_runs}...")
        
        # Teste de Inserção
        tracemalloc.start()
        start_time = time.perf_counter()
        
        # Recria a árvore para cada rodada
        tree_instance = type(tree)() 
        for item in data_to_insert:
            tree_instance.insert(item)
            
        end_time = time.perf_counter()
        
        snapshot = tracemalloc.take_snapshot()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        insert_times.append(end_time - start_time)
        insert_memories.append(peak / 1024) # Converte para KB
        
        # Teste de Busca
        tracemalloc.start()
        start_time = time.perf_counter()
        
        for item in data_to_search:
            tree_instance.search(item)
            
        end_time = time.perf_counter()
        
        snapshot = tracemalloc.take_snapshot()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        search_times.append(end_time - start_time)
        search_memories.append(peak / 1024) # Converte para KB
        
    avg_insert_time = sum(insert_times) / num_runs
    avg_search_time = sum(search_times) / num_runs
    avg_insert_mem = sum(insert_memories) / num_runs
    avg_search_mem = sum(search_memories) / num_runs
    
    return {
        'avg_insert_time': avg_insert_time,
        'avg_search_time': avg_search_time,
        'avg_insert_mem': avg_insert_mem,
        'avg_search_mem': avg_search_mem
    }

## Execução Principal
if __name__ == "__main__":
    
    data_volumes = [10000, 50000, 100000, 200000] # Volumes de dados para teste de desempenho
    
    print("Iniciando a análise comparativa entre BST e AVL...")
    print("--------------------------------------------------")
    
    # Listas para os dados dos gráficos
    bst_insert_times = []
    bst_search_times = []
    bst_insert_mem = []
    bst_search_mem = []
    
    avl_insert_times = []
    avl_search_times = []
    avl_insert_mem = []
    avl_search_mem = []
    
    for size in data_volumes:
        
        # Testa a BST
        bst_tree = BinaryTree()
        bst_results = run_tests(bst_tree, size)
        
        bst_insert_times.append(bst_results['avg_insert_time'])
        bst_search_times.append(bst_results['avg_search_time'])
        bst_insert_mem.append(bst_results['avg_insert_mem'])
        bst_search_mem.append(bst_results['avg_search_mem'])
        
        # Testa a AVL
        avl_tree = AVLTree()
        avl_results = run_tests(avl_tree, size)
        
        avl_insert_times.append(avl_results['avg_insert_time'])
        avl_search_times.append(avl_results['avg_search_time'])
        avl_insert_mem.append(avl_results['avg_insert_mem'])
        avl_search_mem.append(avl_results['avg_search_mem'])

    print("\n\n=============== Gerando Gráficos de Comparação ===============")
    
    # Gráfico 1: Tempo de Inserção
    plt.figure(figsize=(10, 6))
    plt.plot(data_volumes, bst_insert_times, label='BST', marker='o')
    plt.plot(data_volumes, avl_insert_times, label='AVL', marker='o')
    plt.xlabel('Volume de Dados (N)')
    plt.ylabel('Tempo Médio de Inserção (s)')
    plt.title('Comparação de Tempo de Inserção: BST vs. AVL')
    plt.legend()
    plt.grid(True)
    plt.xticks(data_volumes)
    plt.tight_layout()
    plt.savefig('comparacao_tempo_insercao.png')
    
    # Gráfico 2: Tempo de Busca
    plt.figure(figsize=(10, 6))
    plt.plot(data_volumes, bst_search_times, label='BST', marker='o')
    plt.plot(data_volumes, avl_search_times, label='AVL', marker='o')
    plt.xlabel('Volume de Dados (N)')
    plt.ylabel('Tempo Médio de Busca (s)')
    plt.title('Comparação de Tempo de Busca: BST vs. AVL')
    plt.legend()
    plt.grid(True)
    plt.xticks(data_volumes)
    plt.tight_layout()
    plt.savefig('comparacao_tempo_busca.png')

    # Gráfico 3: Consumo de Memória (Inserção)
    plt.figure(figsize=(10, 6))
    plt.plot(data_volumes, bst_insert_mem, label='BST', marker='o')
    plt.plot(data_volumes, avl_insert_mem, label='AVL', marker='o')
    plt.xlabel('Volume de Dados (N)')
    plt.ylabel('Consumo de Memória (KB)')
    plt.title('Comparação de Consumo de Memória (Inserção): BST vs. AVL')
    plt.legend()
    plt.grid(True)
    plt.xticks(data_volumes)
    plt.tight_layout()
    plt.savefig('comparacao_memoria_insercao.png')

    # Gráfico 4: Consumo de Memória (Busca)
    plt.figure(figsize=(10, 6))
    plt.plot(data_volumes, bst_search_mem, label='BST', marker='o')
    plt.plot(data_volumes, avl_search_mem, label='AVL', marker='o')
    plt.xlabel('Volume de Dados (N)')
    plt.ylabel('Consumo de Memória (KB)')
    plt.title('Comparação de Consumo de Memória (Busca): BST vs. AVL')
    plt.legend()
    plt.grid(True)
    plt.xticks(data_volumes)
    plt.tight_layout()
    plt.savefig('comparacao_memoria_busca.png')
    
    print("\nGráficos gerados com sucesso.")

    # Agrupa os resultados em um dicionário para passar para a função de relatório
    final_results = {
        'bst': {
            'insert_times': bst_insert_times,
            'search_times': bst_search_times,
            'insert_mem': bst_insert_mem,
            'search_mem': bst_search_mem
        },
        'avl': {
            'insert_times': avl_insert_times,
            'search_times': avl_search_times,
            'insert_mem': avl_insert_mem,
            'search_mem': avl_search_mem
        }
    }
    
    # Chama a função para gerar o relatório HTML
    generate_html_report(final_results, data_volumes)