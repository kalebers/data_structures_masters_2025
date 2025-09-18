import random
import string
import time
import tracemalloc
import copy

from person import generate_random_persons
from generate_html import generate_html

from sorting import bubble_sort, insertion_sort, selection_sort, quick_sort, quicksort_inplace
from searching import sequential_search, binary_search

# Garantir replicabilidade
random.seed(42)

# Tamanho dos Arrays
sizes = [10000, 50000, 100000] 

# Número de rodadas por método e tamanho de array
number_of_rounds = 5

# Armazenar resultados:
results_per_size = {}

sort_algorithms = [
    #('Bubble Sort', bubble_sort),
    #('Insertion Sort', insertion_sort),
    ('Selection Sort', selection_sort),
    ('Quick Sort', quick_sort),
    ('Quick Sort Inplace', quicksort_inplace)
]

search_algorithms = [
    ('Binary search', binary_search),
    ('Sequential search', sequential_search)
]

# Executa e grava dados de algoritmos de Ordenação
for size in sizes:
    results_per_size[size] = { "time": {}, "used_memory": {} }
    
    print (f"\n\nGerando array de tamanho {size:6d}")
    base_array = generate_random_persons(size)
    
    for name, sorting_algorithm in sort_algorithms:
        print (f"\nExecutando algoritmo {name}", end='')

        results_per_size[size]["time"][name] = []
        results_per_size[size]["used_memory"][name] = []

        for i in range(number_of_rounds):
            print ('.', end='')
            
            arr_copy = copy.deepcopy(base_array)
            
            tracemalloc.start()
            start_time = time.perf_counter()
    
            arr_copy = sorting_algorithm(arr_copy)
            
            end_time = time.perf_counter()
            
            snapshot = tracemalloc.take_snapshot()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            results_per_size[size]["time"][name].append(end_time - start_time)
            results_per_size[size]["used_memory"][name].append(peak / 1024) # Converte para KB


html = generate_html(results_per_size, "Ordenação")

print(f"\n {html}")

# Salvar em arquivo
with open("resultados_sort.html", "w", encoding="utf-8") as f:
    f.write(html)

# Executa e grava dados de algoritmos de Busca
for size in sizes:    
    results_per_size[size] = { "time": {}, "used_memory": {} }

    print (f"\n\nGerando array de tamanho {size:6d}")
    base_array = generate_random_persons(size)
    sorted_array = quicksort_inplace(copy.deepcopy(base_array))
    
    cases = [
        ('Lowest value search', sorted_array[0].matricula),
        ('Highest value search', sorted_array[-1].matricula),
        ('Middle value search', sorted_array[size//2].matricula)
    ]
    
    array_status = [ 'Sorted', 'Unsorted' ]

    for case, target_value in cases:
        for sorted in array_status:

            for name, searching_algorithm in search_algorithms:
                print (f"\nExecutando algoritmo {name} com {size}", end='')

                results_per_size[size]["time"][f"{name} - {case} on {sorted} array"] = []
                results_per_size[size]["used_memory"][f"{name} - {case} on {sorted} array"] = []

                for i in range(number_of_rounds):
                    # Busca binária só funciona em arrays ordenados
                    if (name == 'Binary search' and sorted == 'Unsorted'):
                        break

                    print ('.', end='')
                                        
                    if sorted == 'Unsorted':
                        arr_to_search = base_array
                    else:
                        arr_to_search = sorted_array
                    
                    tracemalloc.start()
                    start_time = time.perf_counter()
            
                    search = searching_algorithm(arr_copy, target_value)
                    
                    end_time = time.perf_counter()
                    
                    snapshot = tracemalloc.take_snapshot()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
                    
                    results_per_size[size]["time"][f"{name} - {case} on {sorted} array"].append(end_time - start_time)
                    results_per_size[size]["used_memory"][f"{name} - {case} on {sorted} array"].append(peak / 1024) 

html = generate_html(results_per_size, "Busca")

print(f"\n {html}")

# Salvar em arquivo
with open("resultados_search.html", "w", encoding="utf-8") as f:
    f.write(html)