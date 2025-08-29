# TODO: Falta Notacao Big O (conferir se está correto - valores parecem estar iguais em todas iteracoes)
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

# -------------------------------
# Gerador de dados fictícios
# -------------------------------
def gerar_registros(n):
    registros = []
    for _ in range(n):
        matricula = ''.join(random.choices(string.digits, k=9))
        nome = ''.join(random.choices(string.ascii_uppercase, k=7))
        salario = round(random.uniform(1500, 20000), 2)
        setor = random.randint(1, 100)
        registros.append((matricula, {"nome": nome, "salario": salario, "setor": setor}))
    return registros

# -------------------------------
# Funções Hash
# -------------------------------
def hash_func1(key, M):
    """Soma dos valores ASCII dos caracteres"""
    "Mostrar a forma mais basica possivel, por gerar muitos"
    "agrupamentos quando chaves tem mesmos caracteres."
    "Serve como baseline"
    return sum(ord(c) for c in key) % M

def hash_func2(key, M):
    """Hash polinomial base 31"""
    "Por 31 ser um número primo, ajuda na dispersão dos valores."
    "Sendo assim, tem melhor distribuição que a soma simples."
    "Pode concentrar colisões se as chaves tiverem padrões semelhantes."
    h = 0
    for c in key:
        h = (31 * h + ord(c)) % M
    return h

def hash_func3(key, M):
    """Multiplicative Hashing (Knuth)"""
    "Ideia de mostrar como se fosse uma matricula de 9 digitos. "
    "Multiplica por um numero irracional porque ajuda espalhar os números deforma"
    "uniforme no espaço de hashing."
    "A ideia é que a multiplicação por um número irracional ajuda a evitar padrões."
    "Precisa que a chave seja tratada como número"
    A = 0.6180339887
    k = int(key)
    return int(M * ((k * A) % 1))

# -------------------------------
# Estrutura da Tabela Hash
# -------------------------------
class HashTable:
    def __init__(self, M, hash_func):
        self.M = M
        self.table = [[] for _ in range(M)]
        self.hash_func = hash_func
        self.colisoes = 0
        self.insercoes = 0

    def insert(self, key, value):
        h = self.hash_func(key, self.M)
        bucket = self.table[h]
        if len(bucket) > 0:
            self.colisoes += 1
        bucket.append((key, value))
        self.insercoes += 1

    def search(self, key):
        h = self.hash_func(key, self.M)
        for k, v in self.table[h]:
            if k == key:
                return v
        return None

    def load_factor(self):
        return self.insercoes / self.M

# -------------------------------
# Experimentos
# -------------------------------
def rodar_experimento(N, M, hash_func, rodadas=5):
    colisoes, load_factors, tempos, mem_usages, cpu_times = [], [], [], [], []

    for _ in range(rodadas):
        registros = gerar_registros(N)

        tracemalloc.start()
        start_cpu = time.process_time()
        start_time = time.time()

        ht = HashTable(M, hash_func)
        for k, v in registros:
            ht.insert(k, v)

        elapsed_time = time.time() - start_time
        cpu_time = time.process_time() - start_cpu
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        process = psutil.Process(os.getpid())
        mem_usage = process.memory_info().rss / (1024 * 1024)  # MB

        # Coleta métricas
        colisoes.append(ht.colisoes)
        load_factors.append(ht.load_factor())
        tempos.append(elapsed_time)
        mem_usages.append(mem_usage)
        cpu_times.append(cpu_time)

    return {
        "colisoes_media": statistics.mean(colisoes),
        "colisoes_dp": statistics.pstdev(colisoes),
        "load_media": statistics.mean(load_factors),
        "tempo_medio": statistics.mean(tempos),
        "tempo_dp": statistics.pstdev(tempos),
        "memoria_media_MB": statistics.mean(mem_usages),
        "cpu_time_medio": statistics.mean(cpu_times),
    }

def mostrar_big_o(N, M):
    print("\n--- Notação Big O ---")
    print(f"Para N = {N} elementos e M = {M} buckets:")
    print("  - Melhor caso (sem colisão): O(1)")
    print(f"  - Pior caso (todas colisões em um bucket): O({N})")
    print(f"  - Caso médio (listas uniformes): O({round(N/M, 2)}) por operação")
    print("Onde N/M é o tamanho médio de cada lista (bucket).")
    print("Se a função hash for boa e M for grande, espera-se O(1) para operações.")

def salvar_resultados_txt(resultados, filename="resultados_hash.txt"):
    with open(filename, "w") as f:
        for res in resultados:
            N = res["N"]
            M = res["M"]
            funcao = res["funcao"]
            f.write(f"Experimento: N={N}, M={M}, Função={funcao}\n")
            f.write(f"Resultados: {res}\n")
            f.write("--- Notação Big O ---\n")
            f.write(f"  Melhor caso: O(1)\n")
            f.write(f"  Pior caso: O({N})\n")
            f.write(f"  Caso médio: O({round(N/M, 2)})\n")
            f.write("\n")

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    N_values = [10_000, 50_000, 100_000]
    M_values = [100, 1000, 5000]
    hash_functions = {
        "Hash1 (ASCII sum)": hash_func1,
        "Hash2 (Polinomial)": hash_func2,
        "Hash3 (Multiplicative)": hash_func3,
    }

    resultados = []

    for N in N_values:
        for M in M_values:
            for nome, func in hash_functions.items():
                print(f"\n - Rodando experimento N={N}, M={M}, {nome}")
                res = rodar_experimento(N, M, func, rodadas=5)
                res.update({"N": N, "M": M, "funcao": nome})
                resultados.append(res)
                print(res)
            mostrar_big_o(N, M)

    salvar_resultados_txt(resultados)
