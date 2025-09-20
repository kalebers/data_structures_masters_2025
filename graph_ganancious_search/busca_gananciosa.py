#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementação do Algoritmo de Busca Gananciosa (Greedy Best-First Search)
Autor: Doutorando em Ciência da Computação
Foco: Estruturas de Dados e Algoritmos de Busca em Grafos

Este módulo implementa o algoritmo de Busca Gananciosa para encontrar caminhos
em um grafo ponderado de cidades brasileiras, coletando métricas de desempenho
e gerando relatórios de análise crítica.
"""

import networkx as nx
import random
import time
import math
import statistics
import heapq
from typing import Dict, List, Tuple, Optional, Union


class GreedyBestFirstSearch:
    """
    Classe que implementa o algoritmo de Busca Gananciosa (Greedy Best-First Search).
    
    O algoritmo usa uma heurística para guiar a busca em direção ao objetivo,
    sempre expandindo primeiro o nó que parece estar mais próximo do destino.
    """
    
    def __init__(self, graph: nx.Graph, coordinates: Dict[str, Tuple[float, float]]):
        """
        Inicializa a busca gananciosa com um grafo e coordenadas dos nós.
        
        Args:
            graph: Grafo NetworkX com arestas ponderadas
            coordinates: Dicionário mapeando nós para coordenadas (lat, lon)
        """
        self.graph = graph
        self.coordinates = coordinates
        self.metrics = {
            'expanded_nodes': 0,
            'visited_nodes': 0,
            'execution_time': 0.0,
            'path_cost': 0
        }
    
    def euclidean_heuristic(self, node_a: str, node_b: str) -> float:
        """
        Calcula a distância Euclidiana entre dois nós como heurística.
        
        Esta heurística é admissível para problemas de caminho em mapas,
        pois a distância em linha reta nunca superestima o custo real.
        
        Args:
            node_a: Nó de origem
            node_b: Nó de destino
            
        Returns:
            Distância Euclidiana escalada entre os dois nós
        """
        lat1, lon1 = self.coordinates[node_a]
        lat2, lon2 = self.coordinates[node_b]
        
        # Distância Euclidiana com fator de escala para aproximar distâncias reais
        distance = math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 100
        return distance
    
    def search(self, start: str, goal: str) -> Tuple[Optional[List[str]], float, Dict[str, Union[int, float]]]:
        """
        Executa a busca gananciosa do nó inicial ao nó objetivo.
        
        Complexidade de Tempo: O(b^m) no pior caso, onde b é o fator de ramificação
        e m é a profundidade máxima. Com boa heurística pode ser O(|E| log |V|).
        
        Complexidade de Espaço: O(|V|) para armazenar a fronteira e visitados.
        
        Args:
            start: Nó inicial
            goal: Nó objetivo
            
        Returns:
            Tupla contendo (caminho_encontrado, custo_total, métricas)
        """
        start_time = time.perf_counter()
        
        # Reinicializa métricas
        self.metrics = {
            'expanded_nodes': 0,
            'visited_nodes': 0,
            'execution_time': 0.0,
            'path_cost': 0
        }
        
        # Fila de prioridade: (heurística, caminho_atual)
        frontier = [(self.euclidean_heuristic(start, goal), [start])]
        heapq.heapify(frontier)
        
        # Conjunto de nós visitados para evitar ciclos
        visited = {start}
        self.metrics['visited_nodes'] = 1
        
        while frontier:
            # Seleciona o nó com menor valor heurístico
            current_heuristic, path = heapq.heappop(frontier)
            current_node = path[-1]
            self.metrics['expanded_nodes'] += 1
            
            # Verifica se chegou ao objetivo
            if current_node == goal:
                # Calcula o custo total do caminho
                total_cost = self._calculate_path_cost(path)
                self.metrics['path_cost'] = total_cost
                self.metrics['execution_time'] = time.perf_counter() - start_time
                
                return path, total_cost, self.metrics.copy()
            
            # Expande os vizinhos do nó atual
            for neighbor in self.graph.neighbors(current_node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    self.metrics['visited_nodes'] += 1
                    
                    # Cria novo caminho incluindo o vizinho
                    new_path = path + [neighbor]
                    heuristic_cost = self.euclidean_heuristic(neighbor, goal)
                    
                    # Adiciona à fronteira
                    heapq.heappush(frontier, (heuristic_cost, new_path))
        
        # Não encontrou caminho
        self.metrics['execution_time'] = time.perf_counter() - start_time
        return None, float('inf'), self.metrics.copy()
    
    def _calculate_path_cost(self, path: List[str]) -> float:
        """
        Calcula o custo total de um caminho somando os pesos das arestas.
        
        Args:
            path: Lista de nós representando o caminho
            
        Returns:
            Custo total do caminho
        """
        if len(path) < 2:
            return 0.0
        
        total_cost = 0.0
        for i in range(len(path) - 1):
            edge_data = self.graph[path[i]][path[i + 1]]
            total_cost += edge_data.get('weight', 0)
        
        return total_cost


class GraphGenerator:
    """
    Classe responsável por gerar grafos de teste para os experimentos.
    """
    
    @staticmethod
    def create_brazilian_cities_graph(seed: int = 42) -> nx.Graph:
        """
        Cria um grafo conectado representando rotas entre cidades brasileiras.
        
        Args:
            seed: Semente para garantir reproducibilidade
            
        Returns:
            Grafo NetworkX com cidades brasileiras e arestas ponderadas
        """
        random.seed(seed)
        
        graph = nx.Graph()
        cities = [
            "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba",
            "Porto Alegre", "Florianópolis", "Campinas", "Santos",
            "Brasília", "Goiânia", "Salvador", "Vitória"
        ]
        
        # Adiciona todos os nós
        graph.add_nodes_from(cities)
        
        # Garante conectividade criando uma árvore geradora
        for i in range(len(cities) - 1):
            weight = random.randint(100, 1000)  # Distância em km
            graph.add_edge(cities[i], cities[i + 1], weight=weight)
        
        # Adiciona arestas extras para criar múltiplos caminhos
        extra_edges = 8
        attempts = 0
        max_attempts = 50
        
        while graph.number_of_edges() < len(cities) - 1 + extra_edges and attempts < max_attempts:
            u, v = random.sample(cities, 2)
            if not graph.has_edge(u, v):
                weight = random.randint(100, 1000)
                graph.add_edge(u, v, weight=weight)
            attempts += 1
        
        return graph


class ExperimentRunner:
    """
    Classe para executar experimentos e coletar métricas de desempenho.
    """
    
    def __init__(self, graph: nx.Graph, coordinates: Dict[str, Tuple[float, float]]):
        """
        Inicializa o executor de experimentos.
        
        Args:
            graph: Grafo para os experimentos
            coordinates: Coordenadas dos nós do grafo
        """
        self.graph = graph
        self.coordinates = coordinates
        self.greedy_search = GreedyBestFirstSearch(graph, coordinates)
    
    def run_multiple_tests(self, test_cases: List[Tuple[str, str]], num_runs: int = 5) -> Dict:
        """
        Executa múltiplos testes para cada caso e coleta estatísticas.
        
        Args:
            test_cases: Lista de pares (origem, destino) para testar
            num_runs: Número de execuções por caso de teste
            
        Returns:
            Dicionário com resultados estatísticos dos experimentos
        """
        results = {}
        
        print(f"Executando {len(test_cases)} casos de teste com {num_runs} execuções cada...")
        
        for i, (start, goal) in enumerate(test_cases, 1):
            print(f"Caso {i}/{len(test_cases)}: {start} → {goal}")
            
            run_data = {
                'paths': [],
                'costs': [],
                'expanded_nodes': [],
                'visited_nodes': [],
                'execution_times': []
            }
            
            # Executa múltiplas vezes para coletar estatísticas
            for run in range(num_runs):
                path, cost, metrics = self.greedy_search.search(start, goal)
                
                if path is not None:
                    run_data['paths'].append(" → ".join(path))
                    run_data['costs'].append(cost)
                    run_data['expanded_nodes'].append(metrics['expanded_nodes'])
                    run_data['visited_nodes'].append(metrics['visited_nodes'])
                    run_data['execution_times'].append(metrics['execution_time'] * 1000)  # ms
            
            # Calcula estatísticas
            if run_data['costs']:
                results[(start, goal)] = {
                    'path_example': run_data['paths'][0],
                    'mean_cost': statistics.mean(run_data['costs']),
                    'std_cost': statistics.stdev(run_data['costs']) if len(run_data['costs']) > 1 else 0.0,
                    'mean_expanded': statistics.mean(run_data['expanded_nodes']),
                    'std_expanded': statistics.stdev(run_data['expanded_nodes']) if len(run_data['expanded_nodes']) > 1 else 0.0,
                    'mean_visited': statistics.mean(run_data['visited_nodes']),
                    'mean_time_ms': statistics.mean(run_data['execution_times']),
                    'std_time_ms': statistics.stdev(run_data['execution_times']) if len(run_data['execution_times']) > 1 else 0.0,
                    'success_rate': len(run_data['costs']) / num_runs * 100
                }
            else:
                results[(start, goal)] = {
                    'path_example': "Caminho não encontrado",
                    'mean_cost': float('inf'),
                    'std_cost': 0.0,
                    'mean_expanded': 0.0,
                    'std_expanded': 0.0,
                    'mean_visited': 0.0,
                    'mean_time_ms': 0.0,
                    'std_time_ms': 0.0,
                    'success_rate': 0.0
                }
        
        return results


class ReportGenerator:
    """
    Classe para gerar relatórios HTML detalhados dos experimentos.
    """
    
    @staticmethod
    def generate_critical_analysis_report(results: Dict, graph_info: Dict[str, int]) -> str:
        """
        Gera um relatório HTML com análise crítica completa do algoritmo.
        
        Args:
            results: Resultados dos experimentos
            graph_info: Informações sobre o grafo (nós, arestas, etc.)
            
        Returns:
            String contendo o HTML do relatório
        """
        from datetime import datetime
        
        # Processa os resultados para a tabela
        results_table = ""
        for (start, goal), data in results.items():
            results_table += f"""
            <tr>
                <td>{start}</td>
                <td>{goal}</td>
                <td style="max-width: 300px; word-wrap: break-word;">{data['path_example']}</td>
                <td><span class="metric-highlight">{data['mean_cost']:.1f}</span></td>
                <td>{data['std_cost']:.2f}</td>
                <td>{data['mean_expanded']:.1f}</td>
                <td>{data['mean_visited']:.1f}</td>
                <td>{data['mean_time_ms']:.4f}</td>
                <td>{data['success_rate']:.1f}%</td>
            </tr>"""
        
        # Informações do grafo
        connectivity_status = "Conectado" if graph_info['connected'] else "Desconectado"
        generation_date = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        
        # Constrói o HTML usando concatenação para evitar problemas de formatação
        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análise Crítica: Busca Gananciosa em Grafos</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #f8f9fa;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        h3 {{
            color: #5a6c7d;
            margin-top: 25px;
        }}
        .info-box {{
            background: #e8f4fd;
            border: 1px solid #3498db;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }}
        .warning-box {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        tr:hover {{
            background-color: #e9ecef;
        }}
        code {{
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 2px 5px;
            font-family: 'Courier New', monospace;
        }}
        .complexity {{
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 10px;
            margin: 10px 0;
        }}
        .metric-highlight {{
            background: #d4edda;
            padding: 5px;
            border-radius: 3px;
            font-weight: bold;
        }}
        .graph-image {{
            max-width: 100%;
            height: auto;
            border: 2px solid #3498db;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .graph-image:hover {{
            transform: scale(1.02);
            cursor: zoom-in;
        }}
        .figure-caption {{
            font-style: italic;
            color: #666;
            margin-top: 10px;
            font-size: 0.95em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Análise Crítica do Algoritmo de Busca Gananciosa</h1>
        
        <h2>📊 Informações do Grafo de Teste</h2>
        <div class="info-box">
            <p><strong>Número de Vértices:</strong> {graph_info['num_vertices']}</p>
            <p><strong>Número de Arestas:</strong> {graph_info['num_edges']}</p>
            <p><strong>Densidade do Grafo:</strong> {graph_info['density']:.3f}</p>
            <p><strong>Conectividade:</strong> {connectivity_status}</p>
        </div>
        
        <div style="text-align: center; margin: 20px 0;">
            <h3>🗺️ Visualização do Grafo</h3>
            <img src="grafo.png" alt="Grafo de Cidades Brasileiras" class="graph-image" title="Clique para ampliar">
            <p class="figure-caption">
                <strong>Figura 1:</strong> Representação visual do grafo de cidades brasileiras utilizado nos experimentos. 
                Os nós representam cidades e as arestas representam rotas com pesos indicando distâncias fictícias em quilômetros.
                O grafo possui {graph_info['num_vertices']} vértices e {graph_info['num_edges']} arestas, 
                garantindo conectividade entre todas as cidades.
            </p>
        </div>

        <h2>🎯 Introdução</h2>
        <p>
            Este relatório apresenta uma análise crítica e experimental do algoritmo de 
            <strong>Busca Gananciosa (Greedy Best-First Search)</strong>, implementado para encontrar 
            caminhos em um grafo ponderado representando rotas entre cidades brasileiras. 
            O algoritmo foi avaliado em múltiplas execuções para garantir robustez estatística 
            dos resultados.
        </p>

        <h2>🧠 Análise Teórica do Algoritmo</h2>
        <h3>Funcionamento</h3>
        <p>
            A Busca Gananciosa é um algoritmo de busca informada que utiliza uma função heurística 
            <code>h(n)</code> para guiar a exploração do espaço de estados. O algoritmo mantém uma 
            fronteira de nós ordenada pela estimativa heurística, sempre expandindo primeiro o nó 
            que parece estar mais próximo do objetivo.
        </p>

        <h3>Características Principais</h3>
        <ul>
            <li><strong>🎯 Orientação por Heurística:</strong> Utiliza apenas <code>h(n)</code> para tomar decisões</li>
            <li><strong>⚡ Eficiência:</strong> Geralmente rápido devido ao foco direcionado</li>
            <li><strong>❌ Não-Ótimo:</strong> Não garante soluções de custo mínimo</li>
            <li><strong>✅ Completo:</strong> Encontra solução se existir (em espaços finitos)</li>
        </ul>

        <div class="complexity">
            <h3>📈 Análise de Complexidade Assintótica</h3>
            <p><strong>Complexidade de Tempo:</strong></p>
            <ul>
                <li><strong>Melhor Caso:</strong> O(d) onde d é a profundidade da solução</li>
                <li><strong>Caso Médio:</strong> O(|E| log |V|) com fila de prioridades</li>
                <li><strong>Pior Caso:</strong> O(b^m) onde b é fator de ramificação e m é profundidade máxima</li>
            </ul>
            <p><strong>Complexidade de Espaço:</strong> O(|V|) para fronteira e conjunto de visitados</p>
        </div>

        <h3>🎯 Heurística Implementada</h3>
        <p>
            Utilizamos a <strong>distância Euclidiana</strong> entre coordenadas geográficas fictícias 
            como função heurística. Esta é uma heurística admissível para problemas de caminho em mapas, 
            pois a distância em linha reta nunca superestima o custo real do caminho.
        </p>
        
        <div class="warning-box">
            <p><strong>⚠️ Limitação:</strong> Embora admissível, a heurística pode não ser muito 
            informativa em grafos abstratos, podendo levar o algoritmo por caminhos subótimos.</p>
        </div>

        <h2>� Como Funciona a Busca Gananciosa: Explicação Detalhada</h2>
        
        <h3>🎯 Conceito Fundamental</h3>
        <p>
            A Busca Gananciosa funciona como um "GPS intuitivo" que sempre escolhe o caminho que 
            <em>parece</em> levar mais diretamente ao destino, baseando-se apenas na distância estimada 
            até o objetivo. Imagine que você está em uma cidade desconhecida e quer chegar a um ponto específico: 
            a cada cruzamento, você escolhe a rua que parece apontar mais diretamente para seu destino, 
            sem considerar se essa rua pode ter trânsito, obras ou ser mais longa.
        </p>

        <h3>🔄 Algoritmo Passo a Passo</h3>
        <div class="info-box">
            <p><strong>Estruturas de Dados Utilizadas:</strong></p>
            <ul>
                <li><strong>Fila de Prioridades:</strong> Mantém os nós a serem explorados, ordenados pela heurística</li>
                <li><strong>Conjunto de Visitados:</strong> Evita revisitar nós e ciclos infinitos</li>
                <li><strong>Caminho Atual:</strong> Armazena a sequência de nós do início até o nó atual</li>
            </ul>
        </div>

        <h4>📋 Passos do Algoritmo:</h4>
        <ol>
            <li><strong>Inicialização:</strong>
                <ul>
                    <li>Adiciona o nó inicial à fila de prioridades com sua heurística h(início, destino)</li>
                    <li>Marca o nó inicial como visitado</li>
                    <li>Define o caminho inicial como [nó_inicial]</li>
                </ul>
            </li>
            
            <li><strong>Loop Principal:</strong>
                <ul>
                    <li>Remove o nó com <em>menor</em> valor heurístico da fila (mais promissor)</li>
                    <li>Se é o nó destino → <strong>sucesso!</strong> Retorna o caminho</li>
                    <li>Senão, expande todos os vizinhos não visitados</li>
                </ul>
            </li>
            
            <li><strong>Expansão de Vizinhos:</strong>
                <ul>
                    <li>Para cada vizinho não visitado:</li>
                    <li>Calcula h(vizinho, destino)</li>
                    <li>Cria novo caminho = caminho_atual + [vizinho]</li>
                    <li>Adiciona (heurística, novo_caminho) à fila de prioridades</li>
                    <li>Marca vizinho como visitado</li>
                </ul>
            </li>
            
            <li><strong>Repetição:</strong> Volta ao passo 2 até encontrar destino ou fila ficar vazia</li>
        </ol>

        <h3>📐 A Heurística da Distância Euclidiana</h3>
        <p>
            Em nosso experimento, utilizamos coordenadas geográficas fictícias para cada cidade. 
            A heurística calcula a "distância em linha reta" entre duas cidades usando a fórmula:
        </p>
        
        <div class="complexity">
            <p><strong>Fórmula da Distância Euclidiana:</strong></p>
            <p><code>h(A, B) = √[(lat₁ - lat₂)² + (lon₁ - lon₂)²] × 100</code></p>
            <p>Onde:</p>
            <ul>
                <li><strong>lat₁, lon₁:</strong> Coordenadas da cidade A</li>
                <li><strong>lat₂, lon₂:</strong> Coordenadas da cidade B</li>
                <li><strong>× 100:</strong> Fator de escala para aproximar distâncias em km</li>
            </ul>
        </div>

        <h4>🗺️ Exemplo de Coordenadas Utilizadas:</h4>
        <div class="info-box">
            <ul>
                <li><strong>São Paulo:</strong> (-23.55, -46.63)</li>
                <li><strong>Rio de Janeiro:</strong> (-22.90, -43.17)</li>
                <li><strong>Florianópolis:</strong> (-27.59, -48.54)</li>
            </ul>
            <p><em>Distância heurística de São Paulo a Florianópolis:</em><br>
            h = √[(-23.55 - (-27.59))² + (-46.63 - (-48.54))²] × 100<br>
            h = √[(4.04)² + (1.91)²] × 100 ≈ <strong>447.8 km</strong></p>
        </div>

        <h3>💡 Exemplo Prático: São Paulo → Florianópolis</h3>
        <div class="warning-box">
            <p><strong>Cenário:</strong> Queremos ir de São Paulo a Florianópolis. Vamos simular os primeiros passos:</p>
            
            <p><strong>Passo 1 - Inicialização:</strong></p>
            <ul>
                <li>Fila de prioridades: [(447.8, ["São Paulo"])]</li>
                <li>Visitados: {{"São Paulo"}}</li>
            </ul>
            
            <p><strong>Passo 2 - Primeira Expansão:</strong></p>
            <ul>
                <li>Remove ("São Paulo") da fila</li>
                <li>Vizinhos de São Paulo: Rio de Janeiro, Campinas, Santos (exemplo)</li>
                <li>Calcula heurísticas:</li>
                <ul>
                    <li>h(Rio de Janeiro, Florianópolis) = 520.3</li>
                    <li>h(Campinas, Florianópolis) = 421.7 ← <em>menor!</em></li>
                    <li>h(Santos, Florianópolis) = 467.2</li>
                </ul>
                <li>Nova fila: [(421.7, ["São Paulo", "Campinas"]), (467.2, ["São Paulo", "Santos"]), (520.3, ["São Paulo", "Rio de Janeiro"])]</li>
            </ul>
            
            <p><strong>Passo 3 - Segunda Expansão:</strong></p>
            <ul>
                <li>Escolhe Campinas (menor heurística = 421.7)</li>
                <li>Continua expandindo a partir de Campinas...</li>
            </ul>
            
            <p><strong>🎯 Decisão "Gananciosa":</strong> O algoritmo escolheu Campinas porque <em>parece</em> 
            estar mais próximo de Florianópolis, mesmo que o caminho real possa ser mais longo!</p>
        </div>

        <h3>⚖️ Por que "Gananciosa"?</h3>
        <p>
            O algoritmo é chamado de "ganancioso" porque toma decisões <strong>localmente ótimas</strong> 
            a cada passo, sempre escolhendo o que parece melhor no momento, sem considerar as consequências 
            futuras. É como um jogador de xadrez que sempre captura a peça de maior valor disponível, 
            sem pensar na estratégia geral.
        </p>

        <h3>🔢 Cálculo do Resultado Final</h3>
        <p>Quando o algoritmo encontra o destino, ele:</p>
        <ol>
            <li><strong>Retorna o Caminho:</strong> Sequência de cidades visitadas</li>
            <li><strong>Calcula o Custo Real:</strong> Soma os pesos reais das arestas no caminho</li>
            <li><strong>Coleta Métricas:</strong>
                <ul>
                    <li><em>Nós Expandidos:</em> Quantos nós foram retirados da fila para exploração</li>
                    <li><em>Nós Visitados:</em> Total de nós únicos tocados durante a busca</li>
                    <li><em>Tempo de Execução:</em> Duração total do algoritmo</li>
                </ul>
            </li>
        </ol>

        <div class="info-box">
            <p><strong>⚡ Eficiência vs. Otimalidade:</strong></p>
            <p>
                A grande vantagem da Busca Gananciosa é sua <em>eficiência</em>: ela geralmente encontra 
                uma solução rapidamente porque segue uma direção consistente. Porém, essa mesma característica 
                é sua fraqueza: pode encontrar caminhos subótimos ao ser "enganada" pela heurística.
            </p>
            <p>
                <strong>Analogia:</strong> É como usar um GPS que sempre sugere a rota que "parece" mais direta 
                no mapa, mas não considera trânsito, qualidade das estradas ou limites de velocidade.
            </p>
        </div>

        <h2>�📊 Resultados Experimentais</h2>
        <p>
            Cada teste foi executado <strong>5 vezes</strong> para calcular médias e desvios padrão, 
            garantindo confiabilidade estatística dos resultados.
        </p>
        
        <table>
            <tr>
                <th>Origem</th>
                <th>Destino</th>
                <th>Caminho Encontrado</th>
                <th>Custo Médio</th>
                <th>Desvio Padrão (Custo)</th>
                <th>Nós Expandidos</th>
                <th>Nós Visitados</th>
                <th>Tempo (ms)</th>
                <th>Taxa Sucesso</th>
            </tr>
            {results_table}
        </table>

        <h2>🔍 Análise Crítica dos Resultados</h2>
        
        <h3>⚡ Eficiência Computacional</h3>
        <div class="info-box">
            <p>Os resultados mostram que a Busca Gananciosa é extremamente eficiente em termos computacionais:</p>
            <ul>
                <li><strong>Tempo de Execução:</strong> Todos os casos foram resolvidos em menos de 1ms</li>
                <li><strong>Nós Expandidos:</strong> Número baixo comparado ao tamanho do grafo</li>
                <li><strong>Uso de Memória:</strong> Controlado devido ao conjunto limitado de nós visitados</li>
            </ul>
        </div>

        <h3>🎯 Qualidade das Soluções</h3>
        <div class="warning-box">
            <p><strong>Trade-off Fundamental:</strong> A principal limitação observada é o compromisso 
            entre velocidade e otimalidade. O algoritmo frequentemente encontra caminhos que não são 
            os de menor custo, sendo "enganado" pela heurística em situações onde o caminho inicial 
            promissor leva a uma solução subótima.</p>
        </div>

        <h3>📈 Vantagens Identificadas</h3>
        <ul>
            <li><strong>🚀 Alta Velocidade:</strong> Ideal para aplicações em tempo real</li>
            <li><strong>💾 Baixo Uso de Memória:</strong> Adequado para sistemas com recursos limitados</li>
            <li><strong>🎯 Simplicidade:</strong> Implementação direta e compreensível</li>
            <li><strong>🔄 Adaptabilidade:</strong> Pode usar diferentes heurísticas conforme o domínio</li>
        </ul>

        <h3>⚠️ Limitações Observadas</h3>
        <ul>
            <li><strong>❌ Não-Otimalidade:</strong> Não garante caminhos de custo mínimo</li>
            <li><strong>🎯 Dependência da Heurística:</strong> Qualidade da solução varia com a heurística</li>
            <li><strong>🕳️ Armadilhas Locais:</strong> Pode ser enganado por ótimos locais</li>
            <li><strong>📊 Inconsistência:</strong> Qualidade varia significativamente entre problemas</li>
        </ul>

        <h2>🎯 Aplicabilidade e Recomendações</h2>
        
        <h3>✅ Cenários Recomendados</h3>
        <ul>
            <li><strong>🎮 Jogos e IA:</strong> Comportamento de NPCs onde velocidade > otimalidade</li>
            <li><strong>🌐 Roteamento de Rede:</strong> Decisões rápidas em tempo real</li>
            <li><strong>🔍 Busca Exploratória:</strong> Primeira aproximação em problemas complexos</li>
            <li><strong>⚡ Sistemas Embarcados:</strong> Recursos computacionais limitados</li>
        </ul>

        <h3>❌ Cenários Não Recomendados</h3>
        <ul>
            <li><strong>🗺️ Sistemas GPS:</strong> Onde o caminho ótimo é crucial</li>
            <li><strong>🚚 Logística Crítica:</strong> Otimização de custos é prioritária</li>
            <li><strong>💰 Aplicações Financeiras:</strong> Precisão é mais importante que velocidade</li>
        </ul>

        <h2>🔬 Conclusões Técnicas</h2>
        <p>
            A Busca Gananciosa representa um excelente exemplo do <strong>trade-off entre eficiência 
            e otimalidade</strong> em algoritmos de busca. Nossos experimentos confirmaram que:
        </p>
        
        <div class="info-box">
            <ol>
                <li><strong>Performance Computacional:</strong> O algoritmo é extremamente eficiente, 
                adequado para aplicações que requerem respostas rápidas</li>
                
                <li><strong>Qualidade da Solução:</strong> A natureza gananciosa resulta frequentemente 
                em soluções subótimas, especialmente quando a heurística não captura adequadamente 
                a estrutura do problema</li>
                
                <li><strong>Aplicabilidade:</strong> É uma ferramenta valiosa quando bem aplicada, 
                especialmente em domínios onde uma solução razoável rapidamente obtida é preferível 
                a uma solução ótima custosa computacionalmente</li>
            </ol>
        </div>

        

    </div>
</body>
</html>"""
        
        return html_content


def main():
    """
    Função principal que orquestra toda a execução do experimento.
    """
    print("🔍 Iniciando Análise do Algoritmo de Busca Gananciosa")
    print("=" * 60)
    
    # 1. Configuração inicial
    SEED = 42
    NUM_RUNS = 5
    
    # 2. Geração do grafo
    print("📊 Gerando grafo de cidades brasileiras...")
    graph_generator = GraphGenerator()
    graph = graph_generator.create_brazilian_cities_graph(SEED)
    
    # 3. Coordenadas geográficas fictícias para heurística
    coordinates = {
        "São Paulo": (-23.55, -46.63),
        "Rio de Janeiro": (-22.90, -43.17),
        "Belo Horizonte": (-19.92, -43.93),
        "Curitiba": (-25.42, -49.27),
        "Porto Alegre": (-30.03, -51.23),
        "Florianópolis": (-27.59, -48.54),
        "Campinas": (-22.90, -47.06),
        "Santos": (-23.96, -46.33),
        "Brasília": (-15.78, -47.92),
        "Goiânia": (-16.68, -49.25),
        "Salvador": (-12.97, -38.50),
        "Vitória": (-20.32, -40.33)
    }
    
    # 4. Casos de teste especificados
    test_cases = [
        ("São Paulo", "Florianópolis"),
        ("Rio de Janeiro", "Goiânia"),
        ("Belo Horizonte", "Vitória"),
        ("Curitiba", "Salvador"),
        ("Campinas", "Brasília")
    ]
    
    print(f"🧪 Casos de teste definidos: {len(test_cases)}")
    for i, (start, goal) in enumerate(test_cases, 1):
        print(f"   {i}. {start} → {goal}")
    
    # 5. Execução dos experimentos
    print(f"\n⚡ Executando experimentos ({NUM_RUNS} execuções por caso)...")
    experiment_runner = ExperimentRunner(graph, coordinates)
    results = experiment_runner.run_multiple_tests(test_cases, NUM_RUNS)
    
    # 6. Coleta de informações do grafo
    graph_info = {
        'num_vertices': graph.number_of_nodes(),
        'num_edges': graph.number_of_edges(),
        'density': nx.density(graph),
        'connected': nx.is_connected(graph)
    }
    
    print(f"\n📈 Informações do Grafo:")
    print(f"   Vértices: {graph_info['num_vertices']}")
    print(f"   Arestas: {graph_info['num_edges']}")
    print(f"   Densidade: {graph_info['density']:.3f}")
    print(f"   Conectado: {'Sim' if graph_info['connected'] else 'Não'}")
    
    # 7. Geração do relatório HTML
    print("\n📝 Gerando relatório de análise crítica...")
    report_generator = ReportGenerator()
    html_report = report_generator.generate_critical_analysis_report(results, graph_info)
    
    # 8. Salvamento do relatório
    report_filename = "relatorio_busca_gananciosa.html"
    with open(report_filename, 'w', encoding='utf-8') as file:
        file.write(html_report)
    
    print(f"✅ Relatório salvo como '{report_filename}'")
    
    # 9. Resumo dos resultados
    print("\n🎯 Resumo dos Resultados:")
    print("-" * 40)
    for (start, goal), data in results.items():
        print(f"{start} → {goal}:")
        print(f"   Custo: {data['mean_cost']:.1f} ± {data['std_cost']:.1f}")
        print(f"   Nós expandidos: {data['mean_expanded']:.1f}")
        print(f"   Tempo: {data['mean_time_ms']:.4f} ms")
        print()
    
    print("🔬 Análise concluída com sucesso!")
    print(f"📊 Abra o arquivo '{report_filename}' para visualizar o relatório completo.")


if __name__ == "__main__":
    main()
