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


# HUFFMAN ENCODING

# alphabet is {0,1,...,n-1}, and character j appears frequencies[j] times
# returns a 'parent' array of length 2n-1; parent[u] is the parent node of u,
# and is_left[u] is 1 if u is left child of parent[u] and 0 if right child
# (so we know which character to append in the huffman encoding)
# in the final output, parent[x] will be -1 only for  the root

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


p, is_left = huffman([70, 3, 20, 37])
print(p)
for c in range(4):
    print(huffman_encode(p, is_left, c))

print(" ------ ")

p, is_left = huffman_alternative([70, 3, 20, 37])
print(p)
for c in range(4):
    print(huffman_encode(p, is_left, c))


# C is a collection of sets, and we want to pick as small a subset as possible
# that has the same union
# returns list of indices of which sets were taken
# def greedy_set_cover(C):
#     ret = []
#     uncovered = set()
#     used = [False] * len(C)
#     for S in C:
#         uncovered.update(S)
#     D = [set(S) for S in C]
#     while len(uncovered) > 0:
#         max_intersection = 0
#         best = -1
#         for i in range(len(D)):
#             if not used[i]:
#                 score = len(uncovered & D[i])  # & is set intersection in Python
#                 if score > max_intersection:
#                     max_intersection = score
#                     best = i
#         assert max_intersection != 0
#         ret.append(best)
#         used[best] = True
#         for x in D[best]:
#             uncovered.discard(x)
#     return ret


# 0  1  2  3  4  5  6
# 7  8  9 10 11 12 13
# OPT would take the last two sets, but greedy takes the first three


def greedy_set_cover(C):
    ret = []
    compare = [set(S) for S in C]
    total = set()
    visited = set()
    for s in C:
        total.update(s)
    while len(total) != 0:
        curr_max = -1
        curr_idx = -1
        for idx, s in enumerate(compare):
            if idx not in visited:
                curr = len(total & s)
                if curr > curr_max:
                    curr_max = curr
                    curr_idx = idx
        ret.append(curr_idx)
        visited.add(curr_idx)
        for ele in compare[curr_idx]:
            total.discard(ele)
    return ret


print(greedy_set_cover([
    [0, 7],
    [1, 2, 8, 9],
    [3, 4, 5, 6, 10, 11, 12, 13],
    [0, 1, 2, 3, 4, 5, 6],
    [7, 8, 9, 10, 11, 12, 13]
]))
