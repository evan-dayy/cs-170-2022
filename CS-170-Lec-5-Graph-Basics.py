# GRAPHS
def adj_list_to_matrix(G):
    n = len(G)
    A = [[False] * n for _ in range(len(G))]
    for i in range(len(G)):
        for x in G[i]:
            A[i][x] = True
    return A


def adj_matrix_to_list(A):
    G = [[] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(G)):
            if A[i][j]:
                G[i].append(j)
    return G


# DFS when graph given in adj list representation
# returns list of preorder #'s, postorder #'s, and array component such that
# component[u] is the name of the connected component that vertex u is in
# vertices are named 0,1,...,n-1, and CC labels are also 0,1,2,...
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


G = [
    [1, 2, 3],
    [0],
    [0, 4],
    [0, 5],
    [2, 5],
    [3, 4]
]
pre, post, comp = DFS(G)
print(pre)
print(post)
print(comp)

pre_events = list(map(lambda x: [x, 'pre'], zip(pre, list(range(len(G))))))
print(pre_events)
post_events = list(map(lambda x: [x, 'post'], zip(post, list(range(len(G))))))

events = sorted(pre_events + post_events)

for e in events:
    if e[1] == 'pre':
        print('entering vertex ' + str(e[0][1]))
    else:
        print('exiting vertex ' + str(e[0][1]))
