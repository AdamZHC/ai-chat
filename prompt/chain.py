# route tree node
from matrix import RouteTreeNode, dfs
import numpy as np
from queue import PriorityQueue

# edges
# (type, u, v)
undefined = 1 << 0
customer_provider, peer_peer, provider_customer = 1 << 2, 1 << 3, 1 << 4


def check_customer_provider(state):
    return (state & customer_provider) == customer_provider
def check_peer_peer(state):
    return (state & peer_peer) == peer_peer
def check_provider_customer(state):
    return (state & provider_customer) == provider_customer

class Graph:
    def __init__(self, m, n):
        none = -1
        self.to, self.nex, self.marks, self.hd = (
            np.array([undefined] * m), np.array([undefined] * m), np.array([undefined] * m), np.array([none] * n))
        self.index = 0
    def add_edge(self, u, v, mark):
        self.to[self.index] = v
        self.marks[self.index] += mark
        self.nex[self.index] = self.hd[u]
        self.hd[u] = self.index
        self.index = self.index + 1
class RoutingTreeModel:
    def __init__(self, edges: np.array, N: int, V: int):
        self.N, self.V = N, V
        self.edges = edges
        # init tree
        self.tree = np.array([RouteTreeNode(i) for i in range(N)])
        self.graph = Graph(V, N)
        self.build_graph()

    def build_graph(self):
        graph = self.graph
        edges = self.edges
        for e in edges:
            if e[0] == 0:
                graph.add_edge(e[1], e[2], customer_provider)
                graph.add_edge(e[2], e[1], provider_customer)
            else:
                graph.add_edge(e[1], e[2], peer_peer)
                graph.add_edge(e[2], e[1], peer_peer)

    def bfs_customer_provider(self, nodes: PriorityQueue) -> PriorityQueue:
        graph = self.graph
        tree = self.tree
        # preprocess
        # queue of snapshots
        snapshotQ, q, vis = PriorityQueue(), PriorityQueue(), np.array([False] * self.N)
        while not nodes.empty():
            top = nodes.get()
            q.put(top); vis[top] = True
        while not q.empty():
            top = q.get()
            snapshotQ.put(top)
            curNode = tree[top]
            # 控制优先选择最小的路由
            i = graph.hd[top]
            while i != -1:
                to = graph.to[i]; mark = graph.marks[i]
                if vis[to]:
                    i = graph.nex[i]
                    continue
                if check_customer_provider(mark):
                    q.put(to)
                    vis[to] = True
                    curNode.add_child(tree[to])
                i = graph.nex[i]
        return snapshotQ

    def bfs_peer_peer(self, nodes: PriorityQueue)-> PriorityQueue:
        graph = self.graph
        tree = self.tree
        # preprocess
        snapshotQ, q, vis = PriorityQueue(), PriorityQueue(), np.array([False] * self.N)
        while not nodes.empty():
            top = nodes.get()
            q.put(top); vis[top] = True
        fixedSize = q.qsize()
        # no bow
        for i in range(fixedSize):
            top = q.get()
            curNode = tree[top]
            snapshotQ.put(top)
            i = graph.hd[top]
            while i != -1:
                to = graph.to[i]; mark = graph.marks[i]
                if vis[to]:
                    i = graph.nex[i]
                    continue
                if check_peer_peer(mark):
                    q.put(to)
                    vis[to] = True
                    curNode.add_child(tree[to])
                i = graph.nex[i]
        while not q.empty():
            snapshotQ.put(q.get())
        return snapshotQ

    def bfs_provider_customer(self, nodes: PriorityQueue):
        graph = self.graph
        tree = self.tree
        q, vis = PriorityQueue(), np.array([False] * self.N)
        while not nodes.empty():
            top = nodes.get()
            q.put(top); vis[top] = True
        while not q.empty():
            top = q.get()
            curNode = tree[top]
            i = graph.hd[top]
            while i != -1:
                to = graph.to[i]; mark = graph.marks[i]
                if vis[to]:
                    i = graph.nex[i]
                    continue
                if check_provider_customer(mark):
                    q.put(to)
                    vis[to] = True
                    curNode.add_child(tree[to])
                i = graph.nex[i]
    def execute(self):
        _root = 0; _nodes = PriorityQueue()
        _nodes.put(0)
        self.bfs_provider_customer(self.bfs_peer_peer(self.bfs_customer_provider(_nodes)))
        dfs(self.tree[_root])


if __name__ == '__main__':
    model = RoutingTreeModel(
        edges=np.array([
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
        ]),
        N=100,
        V=200
    )
    model.execute()


