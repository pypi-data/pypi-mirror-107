# Sorting Algorithms

# Available Sorting algorithms
def AvailableSortingAlgorithms():
    """Returns a List of all the Available Sorting Algorithms present in this module"""

    return ["Bitonic Sort", "Bubble Sort", "Bucket Sort",
            "Cocktail Sort a.k.a Cocktail Shaker Sort",
            "Comb Sort", "Counting Sort", "Cycle Sort", "Gnome Sort", "Heap Sort",
            "Insertion Sort", "Merge Sort", "Pigeonhole Sort", "Quick Sort",
            "Radix Sort", "Selection Sort", "Shell Sort", "Strand Sort",
            "Tim Sort"]

# Bitonic Sort
def BitonicSort(arr, start, count, reverse=False):
    ''' start => starting position i.e 0, count => number of elements i.e len(arr)
        Sorts an array using 'Bitonic Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(log²N)
            Worst Case : O(log²N)
            Avg Case : Θ(log²N)
        Space Complexity :-
            Worst Case : O(N*log²N)
    '''

    CheckList = [2**i for i in range((count//2)+1)]

    if count in CheckList:
        if reverse:
            direction = 0
        else:
            direction = 1

        def Merge(arr, start, count, direction):
            def CompAndSwap(arr, i, j, direction):
                if (direction==1 and (arr[i]>arr[j])) or (direction==0 and (arr[i]<arr[j])):
                    arr[i], arr[j] = arr[j], arr[i]

            if count > 1:
                k = int(count/2)

                for i in range(start, start+k):
                    CompAndSwap(arr, i, i+k, direction)

                Merge(arr, start, k, direction)
                Merge(arr, start+k, k, direction)

        if count > 1:
            k = int(count/2)
            BitonicSort(arr, start, k, False)
            BitonicSort(arr, start+k, k, True)
            Merge(arr, start, count, direction)

        return arr
    else:
        raise ValueError("'count' must be an integral power of 2")

# Bubble Sort
def BubbleSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Bubble Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N)            
            Worst Case : O(N²)
            Avg Case : Θ(N²)
        Space Complexity :-
            Worst Case : O(1)
    '''
    length = len(arr)
    
    for i in range(length) :
        for j in range(length-i-1) :
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
    if reverse:
        return arr[::-1]
    else:
        return arr

# Bucket Sort
def BucketSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Bucket Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N+K)           
            Worst Case : O(N²)
            Avg Case : Θ(N+K)
        Space Complexity :-
            Worst Case : O(N)
    '''
    largest, length = max(arr), len(arr)
    size = largest/length
    buckets = [[] for x in range(length)]

    for i in range(length):
        j = int(arr[i]/size)

        if j != length:
            buckets[j].append(arr[i])
        else:
            buckets[length-1].append(arr[i])

    for i in range(length):
        InsertionSort(buckets[i])

    result = []

    for i in range(length):
        result += buckets[i]

    if reverse:
        return result[::-1]
    else:
        return result

# Cocktail Sort a.k.a Cocktail Shaker Sort
def CocktailSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Cocktail Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N)            
            Worst Case : O(N²)
            Avg Case : Θ(N²)
        Space Complexity :-
            Worst Case : O(1)
    '''

    def swap(i, j) : 
        arr[i], arr[j] = arr[j], arr[i]

    upper, lower, no_swap = len(arr)-1, 0, False

    while (not no_swap and upper-lower > 1):
        no_swap = True

        for j in range(lower, upper):
            if arr[j+1] < arr[j]:
                swap(j+1, j)
                no_swap = False

        upper -= 1

        for j in range(upper, lower, -1):
            if arr[j-1] > arr[j]:
                swap(j-1, j)
                no_swap = False

        lower += 1

    if reverse:
        return arr[::-1]
    else:
        return arr

# Comb Sort
def CombSort(arr, reverse = False):
    ''' Returns the Sorted array
        Sorts an array using 'Comb Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N*log(N))            
            Worst Case : O(N²)
            Avg Case : Θ(N²/2ᵖ) p => No. of Increments
        Space Complexity :-
            Worst Case : O(1)
    '''

    gap, shrink, no_swap = len(arr), 1.3, False

    while not no_swap:
        gap = int(gap/shrink)

        if gap < 1:
            gap, no_swap = 1, True
        else:
            no_swap = False

        i = 0

        while (i+gap) < len(arr):
            if arr[i] > arr[i+gap] :
                arr[i], arr[i+gap], no_swap = arr[i+gap], arr[i], False

            i += 1

    if reverse:
        return arr[::-1]
    else:
        return arr

# Counting Sort
def CountingSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Counting Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N+K)            
            Worst Case : O(N+K)
            Avg Case : Θ(N+K)
        Space Complexity :-
            Worst Case : O(K)
    '''

    largest, length = max(arr), len(arr)
    c = [0]*(largest+1)

    for i in range(length):
        c[arr[i]] += 1

    c[0] -= 1

    for i in range(1, largest+1):
        c[i] += c[i-1]

    result = [None]*length

    for x in reversed(arr):
        result[c[x]] = x
        c[x] -= 1

    if reverse:
        return result[::-1]
    else:
        return result

# Cycle Sort
def CycleSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Cycle Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N²)            
            Worst Case : O(N²)
            Avg Case : Θ(N²)
        Space Complexity :-
            Worst Case : O(N)
    '''

    writes = 0
   
    for cycleStart in range(0, len(arr)-1):
        item, pos = arr[cycleStart], cycleStart

        for i in range(cycleStart+1, len(arr)):
            if arr[i] < item:
                pos += 1
     
        if pos == cycleStart:
           continue
     
        while item == arr[pos]:
           pos += 1

        arr[pos], item = item, arr[pos]
        writes += 1
         
        while pos != cycleStart:
           pos = cycleStart

           for i in range(cycleStart+1, len(arr)):
             if arr[i] < item:
               pos += 1
           
           while item == arr[pos]:
             pos += 1

           arr[pos], item = item, arr[pos]
           writes += 1
   
    if reverse:
        return arr[::-1]
    else:
        return arr

# Gnome Sort
def GnomeSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Gnome Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N)
            Worst Case : O(N²)
            Avg Case : Θ(N²)
        Space Complexity :-
            Worst Case : O(1)
    '''

    for pos in range(1, len(arr)):
        while (pos != 0 and arr[pos] < arr[pos-1]):
            arr[pos], arr[pos-1] = arr[pos-1], arr[pos]
            pos -= 1

    if reverse:
        return arr[::-1]
    else:
        return arr

# Heap Sort
def HeapSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Heap Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N*log(N))
            Worst Case : O(N*log(N))
            Avg Case : Θ(N*log(N))
        Space Complexity :-
            Worst Case : O(1)
    '''

    parent = lambda i : (i-1)//2
    left = lambda i : 2*i+1
    right = lambda i : 2*i+2

    def max_heapify(arr, index, size):
        l, r = left(index), right(index)

        if (l < size and arr[l] > arr[index]):
            largest = l
        else :
            largest = index

        if (r < size and arr[r] > arr[largest]):
            largest = r

        if (largest != index):
            arr[largest], arr[index] = arr[index], arr[largest]
            max_heapify(arr, largest, size)

    def build_max_heap(arr):
        length = len(arr)
        start = parent(length-1)

        while start >= 0:
            max_heapify(arr, index=start, size=length)
            start -= 1

    build_max_heap(arr)

    for i in range(len(arr)-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        max_heapify(arr, index=0, size=i)

    if reverse:
        return arr[::-1]
    else:
        return arr

# Insertion Sort
def InsertionSort(arr, reverse=False) :
    ''' Returns the Sorted array
        Sorts an array using 'Insertion Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N)
            Worst Case : O(N²)
            Avg Case : Θ(N²)
        Space Complexity :-
            Worst Case : O(1)
    '''

    for i in range(1, len(arr)):
        key, j = arr[i], i-1

        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        else:
            arr[j+1] = key

    if reverse:
        return arr[::-1]
    else :
        return arr

# Function to check if an array is Sorted
def IsSorted(arr):
    """ Returns True if the array is Sorted in either ascending or descending order;
        False If Not
    """
    
    ascend, descend = True, False

    for i in range(len(arr)-1):
        if (arr[i] < arr[i+1]) and not descend:
            ascend, descend = True, False
        elif (arr[i] > arr[i+1]) and not ascend:
            descend, ascend = True, False
        else:
            return False
    else:
        return True

# Merge Sort
def MergeSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Merge Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N*log(N))
            Worst Case : O(N*log(N))
            Avg Case : Θ(N*log(N))
        Space Complexity :-
            Worst Case : O(N)
    '''

    if len(arr) > 1:
        mid = len(arr)//2
        lefthalf, righthalf = arr[:mid], arr[mid:]
        MergeSort(lefthalf)
        MergeSort(righthalf)
        i = j = k = 0

        while i < len(lefthalf) and j < len(righthalf) :
            if lefthalf[i] < righthalf[j] :
                arr[k] = lefthalf[i]
                i += 1
            else :
                arr[k] = righthalf[j]
                j += 1

            k += 1

        while i < len(lefthalf) :
            arr[k] = lefthalf[i]
            i += 1
            k += 1

        while j < len(righthalf) :
            arr[k] = righthalf[j]
            j += 1
            k += 1

    if reverse:
        return arr[::-1]
    else:
        return arr

# Pigeonhole Sort
def PigeonholeSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Pigeon-Hole Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N+2ᵏ)
            Worst Case : O(N+2ᵏ)
            Avg Case : Θ(N+2ᵏ)
        Space Complexity :-
            Worst Case : O(2ᵏ)
    '''

    def str_mod(s):
        res = s[7:]
        res = res[::-1]
        return res[1:][::-1]

    my_min, my_max = min(arr), max(arr)
    size = my_max-my_min+1
    holes = [0]*size

    for x in arr:
        assert type(x) is int, f"integers only please; got {str_mod(str(type(x)))} {x}"
        holes[x-my_min] += 1

    i = 0

    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            arr[i] = count+my_min
            i += 1

    if reverse:
        return arr[::-1]
    else:
        return arr

# Quick Sort
def QuickSort(arr, start, end, reverse=False):
    ''' start => starting position i.e 0, end => ending position i.e len(arr)
        Sorts an array using 'Quick Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N*log(N))
            Worst Case : O(N²)
            Avg Case : Θ(N*log(N))
        Space Complexity :-
            Worst Case : O(N*log(N))
    '''

    def partition(arr, start, end):
        pivot = arr[start]
        i, j = start+1, end-1

        while True:
            while (i <= j and arr[i] <= pivot):
                i += 1

            while (i <= j and arr[j] >= pivot):
                j -= 1
     
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
            else:
                arr[start], arr[j] = arr[j], arr[start]
                return j

    if (end-start) > 1:
        p = partition(arr, start, end)
        QuickSort(arr, start, p, reverse)
        QuickSort(arr, p+1, end, reverse)

    if reverse:
        return arr[::-1]
    else:
        return arr

# Radix Sort
def RadixSort(arr, base=10, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Radix Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N*K)
            Worst Case : O(N*K)
            Avg Case : Θ(N*K)
        Space Complexity :-
            Worst Case : O(N+K)
    '''

    def key_factory(digit, base):
        def key(arr, index):
            return ((arr[index]//(base**digit)) % base)

        return key

    def counting_sort(arr, largest, key):
        c = [0]*(largest+1)

        for i in range(len(arr)):
            c[key(arr, i)] = c[key(arr, i)]+1

        c[0] -= 1

        for i in range(1, largest+1):
            c[i] += c[i-1] 

        result = [None]*len(arr)

        for i in range(len(arr)-1, -1, -1):
            result[c[key(arr, i)]] = arr[i]
            c[key(arr, i)] = c[key(arr, i)]-1

        return result

    largest, exp = max(arr), 0

    while (base**exp) <= largest:
        arr = counting_sort(arr, base-1, key_factory(exp, base))
        exp += 1

    if reverse:
        return arr[::-1]
    else:
        return arr

# Selection Sort
def SelectionSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Selection Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N²)
            Worst Case : O(N²)
            Avg Case : Θ(N²)
        Space Complexity :-
            Worst Case : O(1)
    '''

    for i in range(0, len(arr)-1):
        smallest = i

        for j in range(i+1, len(arr)):
            if arr[j] < arr[smallest]:
                smallest = j

        arr[i], arr[smallest] = arr[smallest], arr[i]

    if reverse:
        return arr[::-1]
    else:
        return arr

# Shell Sort
def ShellSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Shell Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N)
            Worst Case : O(N²)
            Avg Case : Θ(N*log(N))
        Space Complexity :-
            Worst Case : O(1)
    '''

    def gaps(size):
        length = size.bit_length()

        for k in range(length-1, 0, -1):
            yield 2**k-1

    def insertion_sort_with_gap(gap):
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i-gap

            while (j >= 0 and temp < arr[j]):
                arr[j+gap] = arr[j]
                j -= gap

            arr[j+gap] = temp

    for g in gaps(len(arr)):
        insertion_sort_with_gap(g)

    if reverse:
        return arr[::-1]
    else:
        return arr

# Strand Sort
def StrandSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Strand Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N)
            Worst Case : O(N²)
            Avg Case : Θ(N²)
        Space Complexity :-
            Worst Case : O(N)
    '''

    def merge_list(arr, b):
        out = []

        while len(arr) and len(b):
            if arr[0] < b[0]:
                out.append(arr.pop(0))
            else:
                out.append(b.pop(0))

        out += arr
        out += b

        return out
     
    def strand(arr):
        i, s = 0, [arr.pop(0)]

        while i < len(arr):
            if arr[i] > s[-1]:
                s.append(arr.pop(i))
            else:
                i += 1

        return s

    out = strand(arr)

    while len(arr):
        out = merge_list(out, strand(arr))

    if reverse:
        return out[::-1]
    else:
        return out

# Tim Sort
def TimSort(arr, reverse=False):
    ''' Returns the Sorted array
        Sorts an array using 'Tim Sort' Algorithm
        Time Complexity :-
            Best Case : Ω(N)
            Worst Case : O(N*log(N))
            Avg Case : Θ(N*log(N))
        Space Complexity :-
            Worst Case : O(N)
    '''

    def calcMinRun(n):
        min_merge, r = 32, 0

        while n >= min_merge:
            r |= n & 1
            n >>= 1

        return n+r
     
    def insertionSort(arr, left, right):
        for i in range(left+1, right+1):
            j = i

            while j > left and arr[j] < arr[j-1]:
                arr[j], arr[j-1] = arr[j-1], arr[j]
                j -= 1

    def merge(arr, l, m, r):
        len1, len2 = m-l+1, r-m
        left, right = [], []

        for i in range(0, len1):
            left.append(arr[l+i])

        for i in range(0, len2):
            right.append(arr[m+i+1])
     
        i, j, k = 0, 0, l
         
        while i < len1 and j < len2:
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1 
            else:
                arr[k] = right[j]
                j += 1
     
            k += 1
     
        while i < len1:
            arr[k] = left[i]
            k += 1
            i += 1
     
        while j < len2:
            arr[k] = right[j]
            k += 1
            j += 1

    n = len(arr)
    minRun = calcMinRun(n)
     
    for start in range(0, n, minRun):
        end = min(start+minRun-1, n-1)
        insertionSort(arr, start, end)
 
    size = minRun

    while size < n:
        for left in range(0, n, 2*size):
            mid = min(n-1, left+size-1)
            right = min((left+2*size-1), (n-1))

            if mid < right:
                merge(arr, left, mid, right)
 
        size = 2*size

    if reverse:
        return arr[::-1]
    else:
        return arr