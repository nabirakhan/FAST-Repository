# ------------------------------------------------------------
# (a) FINDING BOTH LARGEST AND SMALLEST ELEMENTS IN AN ARRAY
# ------------------------------------------------------------

def find_min_max(arr, low, high):
    # Base case: Only one element
    if low == high:
        return arr[low], arr[low]
    # Base case: Two elements → one comparison
    elif high == low + 1:
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        else:
            return arr[high], arr[low]
    else:
        # Divide array in half
        mid = (low + high) // 2
        min1, max1 = find_min_max(arr, low, mid)
        min2, max2 = find_min_max(arr, mid + 1, high)
        # Conquer: Combine results
        return min(min1, min2), max(max1, max2)


# Example Execution for (a)
arr = [12, 5, 9, 45, 1, 23, 56, 3, 88, 7]
mn, mx = find_min_max(arr, 0, len(arr) - 1)
print("----- (a) Min and Max Using Divide & Conquer -----")
print("Array:", arr)
print("Minimum Value:", mn)
print("Maximum Value:", mx)

"""
Recurrence Relation:
    T(n) = 2T(n/2) + 2   with T(2) = 1
Solution:
    T(n) = 3n/2 - 2  comparisons

Comparison:
    Brute Force → 2(n - 1) comparisons
    Divide & Conquer → 1.5n - 2 comparisons
Hence, Divide and Conquer uses fewer comparisons.
"""

# ------------------------------------------------------------
# (b) DIVIDE AND CONQUER EXPONENTIATION (a^n)
# ------------------------------------------------------------

def power(a, n):
    # Base case
    if n == 0:
        return 1
    # If n is even
    if n % 2 == 0:
        half = power(a, n // 2)
        return half * half
    # If n is odd
    else:
        half = power(a, (n - 1) // 2)
        return a * half * half


# Example Execution for (b)
base = 2
exp = 10
result = power(base, exp)
print("\n----- (b) Exponentiation Using Divide & Conquer -----")
print(f"{base}^{exp} =", result)

"""
Recurrence Relation:
    T(n) = T(n/2) + 1
Solution:
    T(n) = O(log n)

Comparison:
    Brute Force → (n - 1) multiplications
    Divide & Conquer → O(log n) multiplications
Hence, Divide & Conquer exponentiation is exponentially faster.
"""

# ------------------------------------------------------------
# (d) QUICKSORT COMPLEXITY (Theoretical Part)
# ------------------------------------------------------------

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quicksort(left) + middle + quicksort(right)


# Example Execution for (d)
data = [34, 7, 23, 32, 5, 62, 32, 2, 45, 7]
sorted_data = quicksort(data)
print("\n----- (d) Quicksort Example -----")
print("Original Array:", data)
print("Sorted Array:", sorted_data)

"""
QUICKSORT COMPLEXITY:
----------------------
Best Case:
    T(n) = 2T(n/2) + O(n)  → O(n log n)

Worst Case:
    T(n) = T(n - 1) + O(n) → O(n^2)

Hence:
    Best Case = O(n log n)
    Worst Case = O(n^2)
"""

# ------------------------------------------------------------
# END OF PROJECT
# ------------------------------------------------------------
