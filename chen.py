from typing import List, Any, Callable
import math

T = Any

NUMBER_MOVES = 0
NUMBER_COMPARISONS = 0


def is_less(e1: T, e2: T) -> bool:
    global NUMBER_COMPARISONS
    NUMBER_COMPARISONS += 1
    return e1 < e2


def find_next_x_block(A: List[T], x0: int, z: int, y0: int, y: int, k: int, f: int, b1: int, b2: int, is_less: Callable[[T, T], bool]) -> int:
    min1 = 0; min2 = 0; min_values_not_set = True
    m = ((z - x0 - f) // k) * k + f + x0
    if m <= z: m += k
    i = m
    if y > y0 and z > x0: i = max(i, y0-2*k) # optimization
    while i + k <= y:
        if i != b1 and i != b2:
            j = m - 1 if i < b1 and b1 < i + k else i + k - 1
            if min_values_not_set or ((not is_less(A[min1], A[i])) and (not is_less(A[min2], A[j]))):
                min_values_not_set = False
                min1 = i
                min2 = j
        i += k
    return min1

def merge_band_y(A: List[T], z: int, y: int, yn: int, is_less: Callable[[T, T], bool]):
    global NUMBER_MOVES, NUMBER_COMPARISONS
    while z < y and y < yn:
        j = z
        for i in range(z+1, y):
            if is_less(A[i], A[j]): j = i
        if is_less(A[y], A[j]):
            A[z], A[y] = A[y], A[z]
            y += 1
        else:
            A[z], A[j] = A[j], A[z]
        NUMBER_MOVES += 3
        z += 1
    if z < y:
        A[z:yn] = sorted(A[z:yn]) # for real code we would do this in-place
        K = yn - z
        NUMBER_COMPARISONS += int(1 * K * int(math.log2(K)) - K) # can be achieved using QuickMergeSort
        NUMBER_MOVES += int(3 * K * int(math.log2(K)))


def merge(A: List[T], x0: int, y0: int, yn: int, is_less: Callable[[T, T], bool], is_recursive_call=False, k=None):
    # Note 1: if |M| > |N|, the same implementation is required from right to left to get the same performance and number of comparisons and moves.
    # Note 2: the algorithm could also use binary searching like described in the paper.
    if x0 >= y0 or y0 >= yn:
        return
    assert y0 - x0 >= 2 # seems to be required...
    global NUMBER_MOVES, NUMBER_COMPARISONS
    if k is None:
        k = int(math.sqrt(y0 - x0))
    f = (y0 - x0) % k
    assert f >= 0
    assert y0 - k - f >= 0
    assert y0 - 2*k >= 0
    x = y0 - 2*k if f == 0 else y0 - k - f
    if x < x0: x = x0
    t = A[x]; A[x] = A[x0]; NUMBER_MOVES += 2
    z = x0; y = y0; b1 = x+1; b2 = y0 - k
    while y - z > 2*k:
        assert x0 >= 0
        assert z >= x0
        assert b1 > x0
        assert b1 > z
        assert x > z
        assert (z+1) % k == b1 % k
        assert b1 < y
        assert b2 < y
        if y >= yn or (not is_less(A[y], A[x])):
            A[z] = A[x]; A[x] = A[b1]; x += 1
            if (x - x0) % k == f:
                if z < x - k: b2 = x - k
                x = find_next_x_block(A, x0, z, y0, y, k, f, b1, b2, is_less)
        else:
            A[z] = A[y]; A[y] = A[b1]; y += 1
            if (y - y0) % k == 0: b2 = y - k
        z += 1; A[b1] = A[z]
        NUMBER_MOVES += 3
        if z == x: x = b1
        if z == b2: b2 = 0
        b1 += 1
        assert b1 >= x0
        if (b1 - x0) % k == f:
            b1 = b1 - k if b2 == 0 else b2
    A[z] = t
    if is_recursive_call:
        merge_band_y(A, z, y, yn, is_less)
    else:
        A[z:y] = sorted(A[z:y]) # for real code we would do this in-place
        K = y - z
        NUMBER_COMPARISONS += int(1 * K * int(math.log2(K)) - K) # can be achieved using QuickMergeSort
        NUMBER_MOVES += int(3 * K * int(math.log2(K)))
        k = int(math.sqrt(k))
        merge(A, z, y, yn, is_less, True, k)

RANDOMIZE = True

import random
random.seed(0x1234567)

M = 1_000_000
N = 1_000_000
if RANDOMIZE:
    l = list(range(M+N))
    random.shuffle(l)
    l[:M] = sorted(l[:M])
    l[M:] = sorted(l[M:])
else:
    l = list(range(M)) + list(range(N))
l_sorted = sorted(l)

merge(l, 0, M, len(l), is_less)
print(f"M={M} N={N} M+N={M+N} COMPARISONS={NUMBER_COMPARISONS} ({NUMBER_COMPARISONS / len(l):.04}*(M+N)) MOVES={NUMBER_MOVES} ({NUMBER_MOVES / len(l):.04}*(M+N))")
assert l == l_sorted

"""
Example Outputs:
M=1000000 N=1000000 M+N=2000000 COMPARISONS=2274471 (1.137*(M+N)) MOVES=6060001 (3.03*(M+N))
M=2000000 N=2000000 M+N=4000000 COMPARISONS=4538244 (1.135*(M+N)) MOVES=12093325 (3.023*(M+N))
"""
