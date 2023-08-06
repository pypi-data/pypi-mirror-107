# Searching algorithms

# Available Searching algorithms
def AvailableSearchingAlgorithms():
    """Returns a List of available Searching algorithms present in this module"""
    return ["Binary Search", "Exponential Search", "Fibonacci Search",
            "Interpolation Search", "Jump Search", "Linear Search"]

# Binary search
def BinarySearch(arr, item):
    """ If item is in array, Returns the index of first occurence of the item in the array; Else Returns False.
        Searches for an item using 'Binary Search' algorithm; Requires a Sorted Array.
        Time Complexity :-
            Best Case : Ω(1)
            Worst Case : O(log₂(N))
            Avg Case : Θ(log₂(N))
        Space Complexity :-
            Worst Case : O(1)
    """

    if IsSorted(arr):
        if item in arr:
            start, end = 0, len(arr)-1

            while start<=end:
                middle = (start+end)//2

                if arr[middle] == item:
                    return middle
                elif arr[middle] < item:
                    start = middle+1
                else:
                    end = middle-1
        else:
            return False
    else:
        raise ValueError("Requires a sorted array; but got a random array")

# Exponential Search
def ExponentialSearch(arr, item):
    """ If item is in array, Returns the index of first occurence of the item in the array; Else Returns False.
        Searches for an item using 'Exponential Search' algorithm; Requires a Sorted Array.
        Time Complexity :-
            Best Case : Ω(1)
            Worst Case : O(log(N))
            Avg Case : Θ(log(N))
        Space Complexity :-
            Worst Case : O(1)
    """

    if IsSorted(arr):
        n = len(arr)

        def binarySearch(arr, l, r, item):
            if item in arr:
                while r >= l:
                    mid = l+(r-l)//2
                    
                    if arr[mid] == item:
                        return mid

                    elif arr[mid] > item:
                        r = mid-1
                    else:
                        l = mid+1
            else:
                return False

        if arr[0] == item:
            return 0

        i = 1

        while i < n and arr[i] <= item:
            i *= 2

        return binarySearch(arr, i//2, min(i, n-1), item)
    else:
        raise ValueError("Requires a sorted array; but got a random array")

# Fibonacci Search
def FibonacciSearch(arr, item):
    """ If item is in array, Returns the index of first occurence of the item in the array; Else Returns False.
        Searches for an item using 'Fibonacci Search' algorithm.
        Time Complexity :-
            Best Case : Ω(1)
            Worst Case : O(log(N))
            Avg Case : Θ(log(N))
        Space Complexity :-
            Worst Case : O(1)
    """
    
    if item in arr:
        m2, m1, n = 0, 1, len(arr)
        m = m2+m1

        while (m < n):
            m2, m1 = m1, m
            m = m2+m1

        offset = -1

        while (m > 1):
            i = min(offset+m2, n-1)

            if (arr[i] < item):
                m, m1 = m1, m2
                m2 = m-m1
                offset = i
            elif (arr[i] > item):
                m = m2
                m1 -= m2
                m2 = m-m1
            else:
                return i

        if m1 and (arr[n-1] == item):
            return n-1
    else:
        return False

# Interpolation Search
def InterpolationSearch(arr, item):
    """ If item is in array, Returns the index of first occurence of the item in the array; Else Returns False.
        Searches for an item using 'Interpolation Search' algorithm; Requires a Sorted Array.
        Time Complexity :-
            Best Case : Ω(1)
            Worst Case : O(N)
            Avg Case : Θ(log₂(log₂(N)))
        Space Complexity :-
            Worst Case : O(1)
    """

    if IsSorted(arr):
        if item in arr:
            start, end = 0, len(arr)-1

            while (start<=end):
                pos = start+((end-start)//(arr[end]-arr[start])*(item-arr[start]))

                if arr[pos] == item:
                    return pos
                elif arr[pos] < item:
                    start = pos+1
                else:
                    end = pos-1
        else:
            return False
    else:
        raise ValueError("Requires a sorted array; but got a random array")

# Jump Search
def JumpSearch(arr, item):
    """ If item is in array, Returns the index of first occurence of the item in the array; Else Returns False.
        Searches for an item using 'Jump Search' algorithm; Requires a Sorted Array.
        Time Complexity :-
            Best Case : Ω(1)
            Worst Case : O(√N)
            Avg Case : Θ(√N)
        Space Complexity :-
            Worst Case : O(1)
    """

    if IsSorted(arr):
        n, prev = len(arr), 0
        step = n**0.5

        while arr[int(min(step, n)-1)] < item:
            prev = step
            step += n**0.5

            if prev >= n:
                return False

        while arr[int(prev)] < item:
            prev += 1

            if prev == min(step, n):
                return -1

        index = int(prev)

        if arr[index] == item:
            return index
        else:         
            return False
    else:
        raise ValueError("Requires a sorted array; but got a random array")

# Linear Search
def LinearSearch(arr, item):
    """ If item is in array, Returns the index of first occurence of the item in the array; Else Returns False.
        Searches for an item using 'Linear Search' algorithm.
        Time Complexity :-
            Best Case : Ω(1)
            Worst Case : O(N)
            Avg Case : Θ(N/2)
        Space Complexity :-
            Worst Case : O(1)
    """

    if item in arr:
        for i in range(len(arr)):
            if arr[i] == item:
                return i
    else:
        return False