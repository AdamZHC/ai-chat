import numpy as np
from queue import Queue
# tree class



class RouteTreeNode:
    def __init__(self, value , height: int = -1, children: np.array = np.array([])):
        self.value = value
        self.height = height
        self.children = children
    def set_value(self, value):
        self.value = value
    def set_height(self, height):
        self.height = height
    def add_child(self, node):
        self.children = np.append(self.children, node)

    def get_children(self):
        return self.children


# edges
# (type, u, v)
undefined = 2
customer_provider, peer_peer, provider_customer = 1, 0, -1
N, V = 10, 11
edges = np.array([
    [0, 0, 1],
    [0, 0, 2],
    [0, 0, 3],
    [0, 1, 2],
    [1, 1, 3],
    [0, 1, 4],
    [0, 2, 4],
    [1, 3, 6],
    [1, 4, 5],
    [0, 7, 5],
    [0, 8, 6],
    [0, 9, 7],
    [0, 9, 1]
])



graph = np.zeros((N, N), dtype=int)
# init tree
tree = np.array([RouteTreeNode(i) for i in range(N)])
def build_graph():
    graph.fill(undefined)
    # build_graph via type and node
    for e in edges:
        if e[0] == 0:
            graph[e[1]][e[2]] = customer_provider
            graph[e[2]][e[1]] = provider_customer
        else:
            graph[e[1]][e[2]] = peer_peer
            graph[e[2]][e[1]] = peer_peer
def bfs_customer_provider(root: int) -> Queue:
    # preprocess
    # queue of snapshots
    snapshotQ, q, vis = Queue(), Queue(), np.array([False] * N)
    q.put(root); vis[root] = True
    while not q.empty():
        top = q.get()
        snapshotQ.put(top)
        curNode = tree[top]
        # 控制优先选择最小的路由
        for node in range(N):
            if vis[node]:
                continue
            if graph[top][node] == customer_provider:
                q.put(node)
                vis[node] = True
                curNode.add_child(tree[node])
    return snapshotQ

def bfs_peer_peer(nodes: Queue)-> Queue:
    # preprocess
    snapshotQ, q, vis = Queue(), Queue(), np.array([False] * N)
    while not nodes.empty():
        top = nodes.get()
        q.put(top); vis[top] = True
    fixedSize = q.qsize()
    # no bow
    for i in range(fixedSize):
        top = q.get()
        curNode = tree[top]
        snapshotQ.put(top)
        for node in range(N):
            if vis[node]:
                continue
            if graph[top][node] == peer_peer:
                q.put(node)
                vis[node] = True
                curNode.add_child(tree[node])
    while not q.empty():
        snapshotQ.put(q.get())
    return snapshotQ

def bfs_provider_customer(nodes: Queue):
    q, vis = Queue(), np.array([False] * N)
    while not nodes.empty():
        top = nodes.get()
        q.put(top); vis[top] = True
    while not q.empty():
        top = q.get()
        curNode = tree[top]
        for node in range(N):
            if vis[node]:
                continue
            if graph[top][node] == provider_customer:
                q.put(node)
                vis[node] = True
                curNode.add_child(tree[node])

def dfs(root: RouteTreeNode):
    for i in root.get_children():
        print("father:{}, this:{}".format(root.value, i.value))
        dfs(i)
    print()



if __name__ == '__main__':
    _root = 0; build_graph()
    bfs_provider_customer(bfs_peer_peer(bfs_customer_provider(_root)))
    dfs(tree[_root])






