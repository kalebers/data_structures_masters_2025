def sequential_search(arr, target):
    for i, person in enumerate(arr):
        if person.matricula == target:
            return i
    return -1

# Só funciona em arrays ordenados
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid].matricula == target:
            return mid
        elif arr[mid].matricula < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1