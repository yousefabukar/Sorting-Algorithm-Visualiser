def quick_sort(arr):
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                yield arr
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        yield arr
        return i + 1

    def quick_sort_recursive(arr, low, high):
        if low < high:
            pi = yield from partition(arr, low, high)
            yield from quick_sort_recursive(arr, low, pi - 1)
            yield from quick_sort_recursive(arr, pi + 1, high)

    yield from quick_sort_recursive(arr, 0, len(arr) - 1)