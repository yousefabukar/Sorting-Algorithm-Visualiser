def merge_sort(arr):
    def merge(arr, start, mid, end):
        left = arr[start:mid]
        right = arr[mid:end]
        i, j, k = 0, 0, start

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
            yield arr

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            yield arr

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            yield arr

    def merge_sort_recursive(arr, start, end):
        if end - start > 1:
            mid = (start + end) // 2
            yield from merge_sort_recursive(arr, start, mid)
            yield from merge_sort_recursive(arr, mid, end)
            yield from merge(arr, start, mid, end)

    yield from merge_sort_recursive(arr, 0, len(arr))