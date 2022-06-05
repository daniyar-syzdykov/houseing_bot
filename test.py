import math
def binary_search(arr, n):
    min_p = 0
    max_p = len(arr) - 1
    mid_p = (min_p + max_p) // 2
    for _ in range(int(math.sqrt(len(arr)))):
        if arr[mid_p] < n:
            min_p = mid_p + 1
            mid_p = (min_p + max_p) // 2
        elif arr[mid_p] > n:
            max_p = mid_p - 1
            mid_p = (min_p + max_p) // 2
        elif arr[mid_p] == n:
            return n




nums = [i for i in range(1000000)]
n = 325964
print(binary_search(nums, n))

