from chain import RoutingTreeModel, undefined, peer_peer
from matrix import dfs
from enum import Enum
import numpy as np
from queue import PriorityQueue

hijacked = 1 << 1
def check_hijacked(state):
    return (state & hijacked) == hijacked
class HijackEnum(Enum):
    ERROR_SOURCE = 'error source hijack',
    ERROR_CHAIN = 'error chain hijack',
    ERROR_POLICY = 'error policy hijack',

def isSucceed(last: int, this: int):
    return this >= last

# Hijacking is construction new route

class NodeWrapper:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority
    def __eq__(self, other):
        return self.priority == other.priority
    def __lt__(self, other):
        return self.priority < other.priority
    def __gt__(self, other):
        return self.priority > other.priority


class HijackRouteModel(RoutingTreeModel):

    def __init__(self, edges: np.array, N: int, V: int, hijacker: int, victim: int,
        hijack_edges: np.array, priority_dict: dict,):
        # hijack_edges is the best match.
        # make an agreement that 0 is ths super source.
        RoutingTreeModel.__init__(self, edges, N, V + len(hijack_edges))
        self.hijacker = hijacker
        self.victim = victim
        # It's allowed that only 0 exists in hijack_edges
        self.hijack_edges = hijack_edges
        self.V += len(hijack_edges)
        self.update_route()
        self.priority_dict = priority_dict
    def update_route(self):
        edges = self.hijack_edges
        for e in edges:
            self.graph.add_edge(e[0], e[1], hijacked)

    def bfs_hijacking(self):
        # no snapshots bfs
        # state: undefined -> hijacked -> customer_provider -> peer_peer -> provider_customer
        # preprocess
        graph = self.graph
        tree = self.tree
        _root = 0
        q, vis = PriorityQueue(), [False] * self.N
        q.put(NodeWrapper(_root, self.priority_dict[_root])); vis[_root] = True
        states = [undefined] * self.N
        while not q.empty():
            top = q.get().value
            curState = states[top]
            curNode = tree[top]
            i = graph.hd[top]
            while i != -1:
                to = graph.to[i]
                mark = graph.marks[i]
                i = graph.nex[i]
                if (check_hijacked(curState) and (not check_hijacked(mark))
                        and top != self.hijacker and top != self.victim):
                    continue
                if vis[to]:
                    continue
                if curNode == mark == peer_peer:
                    continue
                if isSucceed(curState, mark):
                    states[to] = mark
                    vis[to] = True; q.put(NodeWrapper(to, self.priority_dict[to]))
                    curNode.add_child(tree[to])
    def execute(self):
        self.bfs_hijacking()

if __name__ == '__main__':
    model = HijackRouteModel(
        edges=np.array([
            [0, 1, 2],
            [0, 1, 3],
            [0, 1, 4],
            [0, 2, 3],
            [1, 2, 4],
            [0, 2, 5],
            [0, 3, 5],
            [1, 4, 7],
            [1, 5, 6],
            [0, 8, 6],
            [0, 9, 7],
            [0, 10, 8],
            [0, 10, 2]
        ]),
        N=100,
        V=200,
        hijacker=6,
        victim=1,
        # hijack logic
        hijack_edges=[
            [0, 1],
            [0, 8], [8, 6],
        ],
        priority_dict={
            0 : 0,
            1 : 1,
            2 : 2,
            3 : 3,
            4 : 4,
            5 : 5,
            6 : 1,
            7 : 0,
            8 : 0,
            9 : 9,
            10: 10,
        },
    )
    model.execute()
    dfs(model.tree[1])
    print("========================")
    dfs(model.tree[6])

