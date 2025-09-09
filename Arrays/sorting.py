def bubble_sort(array):
    length = len(array)
    
    for i in range(length):
        for j in range(length - i - 1):
            if array[j].matricula > array[j + 1].matricula:
                array[j], array[j + 1] = array[j + 1], array[j]
                
    return array

def selection_sort(array):
  length = len(array)
  
  for i in range(length):
    min_idx = i
    for j in range(i + 1, length):
        if array[j].matricula < array[min_idx].matricula:
            min_idx = j
    if min_idx != i:
        array[i], array[min_idx] = array[min_idx], array[i]
        
    return array

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0:
            if arr[j].matricula > key.matricula:
               arr[j + 1] = arr[j]  # desloca
               j -= 1
            else:
               break
        arr[j + 1] = key
    
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    low = [x for x in arr[1:] if x.matricula <= pivot.matricula]
    high = [x for x in arr[1:] if x.matricula > pivot.matricula]

    return quick_sort(low) + [pivot] + quick_sort(high)

# Quick Sort inplace - tem maior otimização de memória   
def quicksort_inplace(arr):
    return _quicksort_inplace(arr, 0, len(arr) - 1)
    
def _quicksort_inplace(arr, start, end):
    if start < end:
        p = split(arr, start, end)
        _quicksort_inplace(arr, start, p - 1)
        _quicksort_inplace(arr, p + 1, end)
        
    return arr

def split(arr, start, end):
    pivot = arr[end]
    i = start - 1

    for j in range(start, end):
        if arr[j].matricula <= pivot.matricula:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[end] = arr[end], arr[i + 1]
    return i + 1

