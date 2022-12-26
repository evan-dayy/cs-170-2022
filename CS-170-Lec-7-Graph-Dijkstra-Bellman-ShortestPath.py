# MIN HEAP
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
                if self.keys[self.arr[2 * i + 2]] < self.keys[self.arr[smallest]]:
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


# each element of G[u] is a list of length 2: [v, w] means there's an edge (u,v)
# of weight w; start from source s
def dijkstra(G, s):
    dist = [float('inf')] * len(G)
    # from_vertex[u] is the name of the vertex immediately before u on the
    # shortest path from s to u
    from_vertex = [-1] * len(G)
    H = MinHeap(len(G))
    for u in range(len(G)):
        H.insert(u, dist[u])
    dist[s] = 0
    H.decrease_key(s, 0)
    while H.size() > 0:
        u = H.delete_min()
        for v, w in G[u]:
            if dist[u] + w < dist[v]:
                from_vertex[v] = u
                dist[v] = dist[u] + w
                H.decrease_key(v, dist[v])
    return dist, from_vertex


# return the actual shortest path, i.e. sequence of vertices, from s to t
def dijkstra_get_path(G, s, t):
    dist, from_vertex = dijkstra(G, s)
    L = [t]
    while L[-1] != s:
        L.append(from_vertex[L[-1]])
    return L[::-1]


G1 = [
    [[1, 4], [2, 2]],
    [[2, 3], [3, 2], [4, 3]],
    [[1, 1], [3, 4], [4, 5]],
    [],
    [[3, 1]]
]
dist, from_vertex = dijkstra(G1, 0)
print("shortest path distances from 0 are " + str(dist))
print("shortest path from 0 to 4 is " + str(dijkstra_get_path(G1, 0, 4)))


# each element of G[u] is a list of length 2: [v, w] means there's an edge (u,v)
# of weight w; start from source s
# returns None, None if negative cycle is detected
def bellman_ford(G, s):
    dist = [float('inf')] * len(G)
    # from_vertex[u] is the vertex immediately before u on the shortest path from
    # s to u
    from_vertex = [-1] * len(G)
    dist[s] = 0
    for i in range(len(G)):
        for u in range(len(G)):
            for v, w in G[u]:
                if dist[u] + w < dist[v]:
                    if i == len(G) - 1:
                        return None, None
                    else:
                        dist[v] = dist[u] + w
                        from_vertex[v] = u
    return dist, from_vertex


# topological sort alternative implementation
# build the topsort as you're doing the DFS, without counting sort


def bellman_ford_DAG(G, s):
    def topological_sort_alternative(G):
        ret = []
        visited = [False] * len(G)

        def explore(u):
            nonlocal visited, ret
            for v, _ in G[u]:
                if not visited[v]:
                    visited[v] = True
                    explore(v)
            ret.append(u)  # note these appends happen in increasing order by postorder#

        for i in range(len(G)):
            if not visited[i]:
                visited[i] = True
                explore(i)

        return ret[::-1]  # reverse ret to get decreasing postorder #

    dist = [float('inf')] * len(G)
    # from_vertex[u] is the vertex immediately before u on the shortest path from
    # s to u
    from_vertex = [-1] * len(G)
    dist[s] = 0
    sort_vertex = topological_sort_alternative(G)

    for u in sort_vertex:
        for v, w in G[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                from_vertex[v] = u
    return dist, from_vertex


def bellman_ford_DAG_get_path(G, s, t):
    dist, from_vertex = bellman_ford_DAG(G, s)
    if dist == None:
        return None
    L = [t]
    while L[-1] != s:
        L.append(from_vertex[L[-1]])
    return L[::-1]


# return the actual shortest path, i.e. sequence of vertices, from s to t
# if negative cycle detected, returns None
def bellman_ford_get_path(G, s, t):
    dist, from_vertex = bellman_ford(G, s)
    if dist == None:
        return None
    L = [t]
    while L[-1] != s:
        L.append(from_vertex[L[-1]])
    return L[::-1]


G2 = [
    [[1, 2], [2, 1]],
    [[2, -2]],
    [[3, 1]],
    []
]
dist, from_vertex = bellman_ford(G2, 1)
print(from_vertex)
print("shortest path distances from 0 are " + str(dist))
print("shortest path from 0 to 2 is " + str(bellman_ford_get_path(G2, 0, 2)))

# now see what Dijkstra thinks
print("(wrong) shortest path distances according to Dijkstra are " + str(dijkstra(G2, 0)[0]))

# dist, from_vertex = bellman_ford_DAG(G2, 0)
# print(from_vertex)
# print("shortest path distances from 0 are " + str(dist))
# print("shortest path from 0 to 2 is " + str(bellman_ford_DAG_get_path(G2, 0, 2)))
