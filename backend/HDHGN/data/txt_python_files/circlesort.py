def circle_sort_backend(A:list, L:int, R:int):
    '''
        >>> L = [3, 2, 8, 28, 2,]
        >>> circle_sort(L)
        3
        >>> print(L)
        [2, 2, 3, 8, 28]
        >>> L = [3, 2, 8, 28,]
        >>> circle_sort(L)
        1
        >>> print(L)
        [2, 3, 8, 28]
    '''
    n = R-L
    if n < 2:
        return 0
    swaps = 0
    m = n//2
    for i in range(m):
        if A[R-(i+1)] < A[L+i]:
            (A[R-(i+1)], A[L+i],) = (A[L+i], A[R-(i+1)],)
            swaps += 1
    if (n & 1) and (A[L+m] < A[L+m-1]):
        (A[L+m-1], A[L+m],) = (A[L+m], A[L+m-1],)
        swaps += 1
    return swaps + circle_sort_backend(A, L, L+m) + circle_sort_backend(A, L+m, R)

def circle_sort(L:list):
    swaps = 0
    s = 1
    while s:
        s = circle_sort_backend(L, 0, len(L))
        swaps += s
    return swaps

