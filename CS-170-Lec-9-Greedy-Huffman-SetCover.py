# MIN HEAP (from lecture 7)
# Python has heapq, but it doesn't support decrease_key.
# You could instead simply never decrease_key and just repeatedly push,
# skipping over heap items later as you delete_min them if you'd already seen
# that item before but with a smaller key (e.g., HW4). Though, that does have
# the downside of making your heap bigger than it really needs to be by having
# redundant items. Instead, we just implement our own binary heap from scratch.

# this heap implementation assumes all values in the heap are in {0,...,N-1}
# for example with Prim or Dijkstra, N would be n
# (this is so we can have a "loc" array where loc[i] is essentially a pointer
#  the location in which i lives in the heap; if one did not know N in advance,
#  one could implement loc as a dict instead)
class MinHeap:
    def __init__(self, N):
        self.N = N
        self.n = 0  # number of elements currently in heap
        # arr represents a binary tree where arr[0] is the item with minimum key
        # and the children of arr[i] live at arr[2*i+1] and arr[2*i+2]
        self.arr = [None] * N
        self.loc = [-1] * N  # i lives at position loc[i] in arr
        self.keys = [float('inf')] * N  # the key of i is keys[i]

    def __heapify_up__(self, i):
        while i != 0:
            x = self.arr[i]
            parent = self.arr[(i - 1) // 2]
            if self.keys[x] >= self.keys[parent]:
                break
            else:
                # swap x with its parent in the heap
                self.arr[i], self.arr[(i - 1) // 2] = self.arr[(i - 1) // 2], self.arr[i]
                self.loc[x] = (i - 1) // 2
                self.loc[parent] = i
                i = (i - 1) // 2

    def __heapify_down__(self, i):
        while 2 * i + 1 < self.n:
            # smallest of arr[i] and its at most two children
            smallest = i
            if self.keys[self.arr[2 * i + 1]] < self.keys[self.arr[i]]:
                smallest = 2 * i + 1
            if 2 * i + 2 < self.n:
                if self.keys[self.arr[2 * i + 1]] < self.keys[self.arr[smallest]]:
                    smallest = 2 * i + 2
            if smallest == i:
                break
            else:
                self.loc[self.arr[i]] = smallest
                self.loc[self.arr[smallest]] = i
                self.arr[i], self.arr[smallest] = self.arr[smallest], self.arr[i]
                i = smallest

    def size(self):
        return self.n

    # insert x with key k
    def insert(self, x, k):
        self.arr[self.n] = x
        self.keys[x] = k
        self.loc[x] = self.n
        self.n += 1
        self.__heapify_up__(self.n - 1)

    def delete_min(self):
        z = self.arr[0]
        self.loc[z] = -1
        self.arr[0] = self.arr[self.n - 1]
        self.loc[self.arr[0]] = 0
        self.n -= 1
        self.__heapify_down__(0)
        return z

    def decrease_key(self, x, k):
        if k < self.keys[x]:
            self.keys[x] = k
            self.__heapify_up__(self.loc[x])

    # return smallest element without deleting it
    def peek_min(self):
        if self.n == 0:
            return None
        else:
            return self.arr[0]


"""
Huffman Encoding Idea: there is a 1-1 corresponding between the prefix-free code and the 
leaf of a full binary tree. The idea is simple
A B C D
         / \
           / \
             / \
Huffman Algorithm:
    always pick the least 2 frequent elements, these two elements must be sibling at the
    bottom of the tree. This can be approved by contradiction - SWAPPing. 
    
    in every iteration, we find the least 2 frequent elements (fi and fj), and treat these two as a 
    whole (fk), then do the iteration again. (ADT: Priority Queue)
    
    Why this is optimized? It is a greedy algorithm. 
"""


def huffman(frequency):
    n = len(frequency)
    parents = [-1] * (n + n - 1)
    is_left = [False] * (n + n - 1)
    cur = n
    H = MinHeap(2 * n - 1)
    for i in range(n):
        H.insert(i, frequency[i])
    while H.size() > 1:
        x = H.delete_min()
        y = H.delete_min()
        parents[x] = cur
        parents[y] = cur
        is_left[x] = True
        H.insert(cur, H.keys[x] + H.keys[y])
        cur += 1
    return parents, is_left


import heapq


def huffman_alternative(frequency):
    n = len(frequency)
    parents = [-1] * (n + n - 1)
    is_left = [False] * (n + n - 1)
    cur = n
    heap = []
    for i in range(n):
        heapq.heappush(heap, [frequency[i], i])
    while len(heap) > 1:
        fx, x = heapq.heappop(heap)
        fy, y = heapq.heappop(heap)
        parents[x] = cur
        parents[y] = cur
        is_left[x] = True
        heapq.heappush(heap, [fx + fy, cur])
        cur += 1
    return parents, is_left


def huffman_encode(parent, is_left, c):
    x = c
    ret = ''
    while parent[x] != -1:
        if is_left[x]:
            ret += '0'
        else:
            ret += '1'
        x = parent[x]
    return ret[::-1]


p, is_left = huffman([4,4,4,4])
print(p)
for c in range(4):
    print(huffman_encode(p, is_left, c))

print(" ------ ")

p, is_left = huffman_alternative([4,4,4,4])
print(p)
for c in range(4):
    print(huffman_encode(p, is_left, c))

