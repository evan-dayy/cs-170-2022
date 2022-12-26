# MIN HEAP (from previous lecture)
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
import heapq


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


# PRIM MST

# each element of G[u] is a list of length 2: [v, w] means there's an edge (u,v)
# of weight w; start from source s, which by default is vertex 0
# returns an MST as a list of edges, where each edge is represented as [u, v]
def prim(G, s=0):
    H = MinHeap(len(G))
    T = []  # list of edges in the MST
    from_vertex = [-1] * len(G)
    for u in range(len(G)):
        H.insert(u, float('inf'))
    H.decrease_key(s, 0)
    while H.size() > 0:
        u = H.delete_min()
        if u != s:
            T.append([from_vertex[u], u])
        for v, w in G[u]:
            if w < H.keys[v]:
                H.decrease_key(v, w)
                from_vertex[v] = u
    return T

    # DISJOINT FOREST FOR UNION FIND
    # (with path compression and union-by-rank)


def prim_alternative(G, s=0):
    visited = {s}
    heap = [(0, s, None)]
    res = []
    while heap:
        _, src, des = heapq.heappop(heap)
        if des:
            if des not in visited:
                res.append([src, des])
                visited.add(des)
        else:
            des = src

        for tar, w in G[des]:
            if tar not in visited:
                heapq.heappush(heap, (w, des, tar))
    return res


class DisjointForest:
    def __init__(self, n):
        self.n = n
        self.rank = [0] * n
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] == x:
            return x
        else:
            y = self.find(self.parent[x])
            self.parent[x] = y
            return y

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x != y:
            if self.rank[x] < self.rank[y]:
                x, y = y, x
            elif self.rank[x] == self.rank[y]:
                self.rank[x] += 1
            self.parent[y] = x


# KRUSKAL

# each element of G[u] is a list of length 2: [v, w] means there's an edge (u,v)
# of weight w
# returns an MST as a list of edges, where each edge is represented as [u, v]
def kruskal(G):
    E = []
    ret = []
    for u in range(len(G)):
        for e in G[u]:
            E.append([e[1], u, e[0]])

    E.sort()
    DF = DisjointForest(len(G))
    for e in E:
        u, v = e[1], e[2]
        if DF.find(u) != DF.find(v):
            DF.union(u, v)
            ret.append([u, v])
    return ret


G = [
    [[1, 1], [2, 1]],
     [[0, 1], [2, 2]],
     [[0, 1], [1, 2]]
]
print(prim(G))
print(prim_alternative(G))
print(kruskal(G))
