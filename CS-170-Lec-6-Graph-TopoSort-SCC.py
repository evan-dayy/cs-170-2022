# DFS code from previous lecture
def DFS(G):
    n = len(G)
    preorder = [None] * n
    postorder = [None] * n
    component = [None] * n
    visited = [False] * n
    clock = 0
    cc_id = 0

    def explore(u):
        nonlocal clock, preorder, postorder, component, visited, cc_id
        component[u] = cc_id
        preorder[u] = clock
        clock += 1
        # for adj matrix representation, replace "for v in G[u]"
        # with "for i in range(len(G)): if A[u][i]: ..."
        for v in G[u]:
            if not visited[v]:
                visited[v] = True
                explore(v)
        postorder[u] = clock
        clock += 1

    cc_id = 0  # connected component ID

    for i in range(n):
        if not visited[i]:
            visited[i] = True
            explore(i)
            cc_id += 1

    return preorder, postorder, component


# topological sort via DFS then sorting by decreasing postorder #, using
# counting sort
def topological_sort(G):
    _, post, _ = DFS(G)
    countsort = [-1] * (2 * len(G))  # postorder numbers are distinct in {1,...,2n-1}
    for u in range(len(G)):
        countsort[post[u]] = u
    ret = []
    for i in range(2 * len(G) - 1, 0, -1):
        if countsort[i] != -1:
            ret.append(countsort[i])
    return ret


# topological sort alternative implementation
# build the topsort as you're doing the DFS, without counting sort
def topological_sort_alternative(G):
    ret = []
    visited = [False] * len(G)

    def explore(u):
        nonlocal visited, ret
        for v in G[u]:
            if not visited[v]:
                visited[v] = True
                explore(v)
        ret.append(u)  # note these appends happen in increasing order by postorder#

    for i in range(len(G)):
        if not visited[i]:
            visited[i] = True
            explore(i)

    return ret[::-1]  # reverse ret to get decreasing postorder


G1 = [
    [1, 2, 3],
    [],
    [4],
    [5],
    [5],
    []
]
print(topological_sort_alternative(G1))


# FIND SCCs

def reverse_graph(G):
    H = [[] for _ in range(len(G))]
    for u in range(len(G)):
        for v in G[u]:
            H[v].append(u)
    return H


# finds the SCCs of G and returns a vector scc_ids of length n
# where scc_ids[u] is the name of the SCC that vertex u is in
def SCC(G):
    # sort by decreasing postorder number in reverse graph
    # sort in O(n) time using Counting Sort
    # Note: calling topological_sort would work, but technically it
    #       isn't necessarily a topsort because G might not be a DAG
    _, post, _ = DFS(reverse_graph(G))
    vertex_order = []
    countsort = [-1] * (2 * len(G))
    for u in range(len(G)):
        countsort[post[u]] = u
    for i in range(2 * len(G) - 1, 0, -1):
        if countsort[i] != -1:
            vertex_order.append(countsort[i])

    # now start doing DFS's to tell which SCC each vertex is in
    scc_ids = [-1] * len(G)
    label = 0

    def explore(u):
        nonlocal label, scc_ids
        for v in G[u]:
            if scc_ids[v] == -1:  # v isn't visited yet
                scc_ids[v] = label
                explore(v)

    for u in vertex_order:
        if scc_ids[u] == -1:
            scc_ids[u] = label
            explore(u)
            label += 1

    return scc_ids


G2 = [
    [1, 3],
    [2, 3, 4],
    [5],
    [],
    [1, 5, 7],
    [2],
    [],
    [6, 8, 9],
    [7],
    [6, 10],
    [11],
    [9]
]
scc_ids = SCC(G2)
num_sccs = max(scc_ids) + 1
SCCs = []
for i in range(num_sccs):
    # all vertices in G2 with SCC ID i
    SCCs.append(list(filter(lambda x: scc_ids[x] == i, range(len(G2)))))
    print('vertices in SCC ' + str(i) + ': ' + str(SCCs[i]))

from collections import deque


# BFS from s
def BFS(G, s):
    n = len(G)
    # shortest path from s to u ends with the edge (from_vertex[u], u)
    from_vertex = [-1] * n
    dist = [float('inf')] * n
    Q = deque()
    Q.append(s)
    dist[s] = 0
    while len(Q) > 0:
        u = Q.popleft()
        for v in G[u]:
            if dist[v] == float('inf'):  # v not visited yet
                dist[v] = dist[u] + 1
                from_vertex[v] = u
                Q.append(v)
    return dist, from_vertex


# returns the actual shortest path, i.e. sequence of vertices, from s to t
def get_path_BFS(G, s, t):
    dist, from_vertex = BFS(G, s)
    if dist[t] == float('inf'):
        return None  # there is no s-t path at all
    else:
        # uncover path in reverse order
        path = [t]
        while path[-1] != s:
            path.append(from_vertex[path[-1]])
        return path[::-1]  # now reverse again to get correct order, starting at s


# Let's find the shortest path from 0 to 5 in G1
# (should go through 3, and not through 2 and 4)
print(get_path_BFS(G1, 0, 5))
