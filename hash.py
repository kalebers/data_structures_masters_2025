# Implementação de Tabela Hash com Encadeamento Separado
 # O que é M? M é o tamanho da tabela hash (número de buckets)
 # O que é N? N é o número de elementos na tabela hash
 # O que é tempo_dp? tempo_dp é o desvio padrão do tempo de execução das operações na tabela hash.
 # o que é colisoes_dp? colisoes_dp é o desvio padrão do número de colisões ocorridas durante as operações na tabela hash.
 
import random
import string
import time
import tracemalloc
import psutil
import os
import statistics
import matplotlib.pyplot as plt

def gerar_registros(n):
    """
    Gera uma lista de registros fictícios com 'n' elementos.
    Cada registro é uma tupla (chave, valor), onde a chave é uma matrícula
    única de 9 dígitos e o valor é um dicionário com nome, salário e setor.
    """
    registros = []
    # Usamos um set para garantir que as matrículas (chaves) sejam únicas,
    # evitando problemas de duplicação durante os testes.
    matriculas_geradas = set()
    for _ in range(n):
        matricula = ''.join(random.choices(string.digits, k=9))
        while matricula in matriculas_geradas:
            matricula = ''.join(random.choices(string.digits, k=9))
        matriculas_geradas.add(matricula)
        nome = ''.join(random.choices(string.ascii_uppercase, k=7))
        salario = round(random.uniform(1500, 20000), 2)
        setor = random.randint(1, 100)
        registros.append((matricula, {"nome": nome, "salario": salario, "setor": setor}))
    return registros

def hash_func1(key, M):
    """
    Função Hash 1: Soma dos valores ASCII dos caracteres.
    É uma função simples e serve como linha de base. Pode gerar muitas colisões,
    especialmente com chaves que têm os mesmos caracteres rearranjados.
    """
    return sum(ord(c) for c in key) % M

def hash_func2(key, M):
    """
    Função Hash 2: Hash polinomial base 31.
    Usamos um número primo (31) ajuda a dispersar melhor os valores,
    reduzindo o número de colisões em comparação com a soma simples.
    """
    h = 0
    for c in key:
        h = (31 * h + ord(c)) % M
    return h

def hash_func3(key, M):
    """
    Função Hash 3: Hashing Multiplicativo (Knuth).
    Esta função é ideal para chaves que são números. Multiplica a chave por
    um número irracional para espalhar os valores uniformemente no espaço de hashing,
    o que é muito eficaz para evitar padrões de dados que causem colisões.
    """
    A = 0.6180339887  # Constante irracional (proporção áurea)
    k = int(key)
    return int(M * ((k * A) % 1))

class HashTable:
    """
    Implementação da Tabela Hash usando encadeamento separado para tratar colisões.
    Esta classe não usa bibliotecas prontas, conforme exigido pelo trabalho.
    """
    def __init__(self, M, hash_func):
        """
        Inicializa a tabela hash com um tamanho 'M' e uma função hash.
        A tabela é uma lista de listas (buckets), onde cada sub-lista
        armazenará os itens que colidem no mesmo índice.
        """
        self.M = M
        self.table = [[] for _ in range(M)]
        self.hash_func = hash_func
        self.insercoes = 0

    def insert(self, key, value):
        """
        Insere um par (chave, valor) na tabela hash.
        Calcula o índice usando a função hash e adiciona o item ao bucket
        correspondente.
        """
        h = self.hash_func(key, self.M)
        self.table[h].append((key, value))
        self.insercoes += 1
        
    def search(self, key):
        """
        Busca um valor na tabela hash pela chave.
        Conta o número de iterações (comparações) realizadas para encontrar o item.
        Retorna o valor e a contagem de iterações, ou None e a contagem.
        """
        h = self.hash_func(key, self.M)
        iteracoes = 0
        for k, v in self.table[h]:
            iteracoes += 1
            if k == key:
                return v, iteracoes
        return None, iteracoes

def rodar_experimento_hash(N, M, hash_func, rodadas=5):
    """
    Executa um experimento completo para uma tabela hash, medindo diversas métricas
    para as operações de inserção e busca. O experimento é repetido 5 vezes
    para obter resultados estatísticos confiáveis.
    """
    # Listas para armazenar as métricas de cada uma das 5 rodadas
    colisoes_list, tempo_insercao_list, tempo_busca_list = [], [], []
    mem_peak_list, cpu_time_list, iteracoes_busca_list = [], [], []

    # Define o número de chaves para buscar (1% dos dados, mínimo de 100)
    num_buscas = max(100, int(N * 0.01))

    for _ in range(rodadas):
        # Gera os dados fictícios para a rodada
        registros = gerar_registros(N)
        # Seleciona chaves aleatórias para buscar
        chaves_busca = random.sample([r[0] for r in registros], num_buscas)

        # --- Medição de INSERÇÃO ---
        tracemalloc.start()  # Inicia a medição de memória
        start_cpu_insert = time.process_time()  # Tempo de CPU
        start_time_insert = time.time()  # Tempo de parede (wall-clock)
        
        ht = HashTable(M, hash_func)
        colisoes_rodada = 0
        for k, v in registros:
            h = ht.hash_func(k, ht.M)
            if len(ht.table[h]) > 0:
                colisoes_rodada += 1  # Conta a colisão antes de inserir
            ht.insert(k, v)
        
        elapsed_time_insert = time.time() - start_time_insert
        cpu_time_insert = time.process_time() - start_cpu_insert
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop() # Finaliza a medição de memória
        
        process = psutil.Process(os.getpid())
        mem_usage_mb = process.memory_info().rss / (1024 * 1024)

        colisoes_list.append(colisoes_rodada)
        tempo_insercao_list.append(elapsed_time_insert)
        mem_peak_list.append(peak / (1024 * 1024)) # Armazena o pico de memória em MB
        cpu_time_list.append(cpu_time_insert)

        # --- Medição de BUSCA ---
        iteracoes_busca_total = 0
        start_time_search = time.time()
        for k_busca in chaves_busca:
            _, iteracoes = ht.search(k_busca)
            iteracoes_busca_total += iteracoes
        
        elapsed_time_search = time.time() - start_time_search
        
        tempo_busca_list.append(elapsed_time_search)
        # Calcula a média de iterações por busca e armazena
        iteracoes_busca_list.append(iteracoes_busca_total / num_buscas)

    # Calcula e retorna as médias e desvios padrão de todas as métricas
    # A análise do desvio padrão é essencial para o relatório,
    # mostrando a variabilidade dos resultados.
    return {
        "N": N,
        "M": M,
        "funcao": hash_func.__name__,
        "colisoes_media": statistics.mean(colisoes_list),
        "colisoes_dp": statistics.pstdev(colisoes_list),
        "tempo_insercao_medio": statistics.mean(tempo_insercao_list),
        "tempo_insercao_dp": statistics.pstdev(tempo_insercao_list),
        "tempo_busca_medio": statistics.mean(tempo_busca_list),
        "tempo_busca_dp": statistics.pstdev(tempo_busca_list),
        "iteracoes_busca_media": statistics.mean(iteracoes_busca_list),
        "iteracoes_busca_dp": statistics.pstdev(iteracoes_busca_list) if len(iteracoes_busca_list) > 1 else 0.0,
        "memoria_pico_media_MB": statistics.mean(mem_peak_list),
        "cpu_time_medio": statistics.mean(cpu_time_list),
        "load_factor": ht.insercoes / ht.M,
    }
    
def plot_resultados(resultados):
    """
    Gera e salva gráficos de comparação para as métricas de desempenho.
    """
    os.makedirs("plots", exist_ok=True) # Cria a pasta 'plots' se não existir

    for N in sorted(list(set(res['N'] for res in resultados))):
        # Filtra resultados para o N atual
        resultados_n = [res for res in resultados if res['N'] == N]
        
        # Agrupa os resultados por função hash e M
        hash_funcs = sorted(list(set(res['funcao'] for res in resultados_n)))
        M_values = sorted(list(set(res['M'] for res in resultados_n)))

        # Plot 1: Tempo de Inserção por Função Hash e M
        plt.figure(figsize=(12, 6))
        for M in M_values:
            tempos = [res['tempo_insercao_medio'] for res in resultados_n if res['M'] == M]
            tempos_dp = [res['tempo_insercao_dp'] for res in resultados_n if res['M'] == M]
            plt.errorbar(hash_funcs, tempos, yerr=tempos_dp, marker='o', label=f'M={M}')
        
        plt.title(f'Tempo Médio de Inserção (N={N})')
        plt.xlabel('Função Hash')
        plt.ylabel('Tempo (segundos)')
        plt.legend(title='Tamanho da Tabela (M)')
        plt.grid(True)
        plt.savefig(f'plots/tempo_insercao_N{N}.png')
        plt.close()

        # Plot 2: Iterações Médias de Busca por Função Hash e M
        plt.figure(figsize=(12, 6))
        for M in M_values:
            iteracoes = [res['iteracoes_busca_media'] for res in resultados_n if res['M'] == M]
            iteracoes_dp = [res['iteracoes_busca_dp'] for res in resultados_n if res['M'] == M]
            plt.errorbar(hash_funcs, iteracoes, yerr=iteracoes_dp, marker='o', label=f'M={M}')
        
        plt.title(f'Média de Iterações por Busca (N={N})')
        plt.xlabel('Função Hash')
        plt.ylabel('Iterações Médias')
        plt.legend(title='Tamanho da Tabela (M)')
        plt.grid(True)
        plt.savefig(f'plots/iteracoes_busca_N{N}.png')
        plt.close()

        # Plot 3: Colisões Totais por Função Hash e M
        plt.figure(figsize=(12, 6))
        for M in M_values:
            colisoes = [res['colisoes_media'] for res in resultados_n if res['M'] == M]
            colisoes_dp = [res['colisoes_dp'] for res in resultados_n if res['M'] == M]
            plt.errorbar(hash_funcs, colisoes, yerr=colisoes_dp, marker='o', label=f'M={M}')
        
        plt.title(f'Colisões Médias na Inserção (N={N})')
        plt.xlabel('Função Hash')
        plt.ylabel('Colisões Médias')
        plt.legend(title='Tamanho da Tabela (M)')
        plt.grid(True)
        plt.savefig(f'plots/colisoes_N{N}.png')
        plt.close()

def salvar_resultados_txt(resultados, filename="resultados_hash.txt"):
    """
    Salva os resultados dos experimentos em um arquivo de texto.
    Inclui uma seção de análise da notação Big-O para cada cenário,
    conforme solicitado no trabalho.
    """
    with open(filename, "w") as f:
        for res in resultados:
            N = res["N"]
            M = res["M"]
            funcao = res["funcao"]
            f.write(f"Experimento: N={N}, M={M}, Função: {funcao}\n")
            f.write(f"Resultados: {res}\n")
            f.write("--- Análise Assintótica (Notação Big-O) ---\n")
            f.write(f"  Melhor caso (inserção/busca): O(1)\n")
            f.write(f"  Pior caso (inserção/busca): O({N})\n")
            f.write(f"  Caso médio (inserção/busca): O(1 + N/M)\n")
            f.write("Onde N/M é o fator de carga e representa o tamanho médio de cada lista (bucket).\n")
            f.write("Se a função hash for boa, espera-se uma performance próxima de O(1).\n")
            f.write("\n")

if __name__ == "__main__":
    """
    Função principal que coordena a execução de todos os experimentos.
    Define os volumes de dados, tamanhos de tabela e funções hash,
    e então itera sobre cada combinação.
    """
    # Volumes de dados a serem testados [cite: 20]
    N_values = [10_000, 50_000, 100_000]
    # Tamanhos de tabela hash para avaliação de colisões e load factor [cite: 26, 27]
    M_values = [100, 1000, 5000]
    # As três funções hash distintas solicitadas [cite: 25]
    hash_functions = {
        "Hash1 (Soma ASCII)": hash_func1,
        "Hash2 (Polinomial)": hash_func2,
        "Hash3 (Multiplicativo)": hash_func3,
    }

    resultados = []

    # Loop principal para rodar todos os cenários de teste
    for N in N_values:
        for M in M_values:
            for nome, func in hash_functions.items():
                print(f"\n- Rodando experimento N={N}, M={M}, Função: {nome}")
                res = rodar_experimento_hash(N, M, func, rodadas=5)
                resultados.append(res)
                print(res)

    # Salva todos os resultados em um arquivo de texto
    salvar_resultados_txt(resultados)

    # Gera e salva os gráficos para a análise visual 
    plot_resultados(resultados)