def dfs_rec(adj, visited, s):
    visited[s] = True

    print(s, end=" ")

    for i in adj[s]:
        if not visited[i]:
            dfs_rec(adj, visited, i)


def dfs(adj, s):
    visited = [False] * len(adj)
    dfs_rec(adj, visited, s)

def add_edge(adj, s, t):
    adj[s].append(t)
    adj[t].append(s)
