import collections
import time


class MinCutSolver:
    """
    implements Edmonds-Karp algorithm for min s-t Cut.
    """

    def __init__(self, vertices_count):
        self.V = vertices_count
        # adjacency list: graph[u][v] = capacity
        self.graph = collections.defaultdict(dict)

    def add_edge(self, u, v, capacity):
        """adds directed edge with capacity."""
        self.graph[u][v] = capacity
        if v not in self.graph:
            self.graph[v] = {}
        if u not in self.graph[v]:
            self.graph[v][u] = 0

    def _bfs(self, r_graph, s, t, parent):
        """
        bfs to find augmenting path in residual graph.
        returns true if path s->t exists.
        """
        visited = {i: False for i in range(self.V)}
        queue = collections.deque([s])
        visited[s] = True
        parent[s] = -1

        while queue:
            u = queue.popleft()

            # iterate neighbors in residual graph
            for v, cap in r_graph[u].items():
                if not visited[v] and cap > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True
        return False

    def solve(self, s, t):
        """
        executes edmonds-karp and extracts min cut.
        returns: (max_flow_value, (partition_s, partition_t), cut_edges)
        """
        r_graph = collections.defaultdict(dict)
        for u in self.graph:
            for v in self.graph[u]:
                r_graph[u][v] = self.graph[u][v]
                if u not in r_graph[v]:
                    r_graph[v][u] = 0

        parent = {}
        max_flow = 0

        # compute max flow
        while self._bfs(r_graph, s, t, parent):
            path_flow = float('inf')
            v = t
            while v != s:
                u = parent[v]
                path_flow = min(path_flow, r_graph[u][v])
                v = u

            max_flow += path_flow
            v = t
            while v != s:
                u = parent[v]
                r_graph[u][v] -= path_flow
                r_graph[v][u] += path_flow
                v = u

        # extract min cut
        visited = {i: False for i in range(self.V)}
        queue = collections.deque([s])
        visited[s] = True

        while queue:
            u = queue.popleft()
            for v, cap in r_graph[u].items():
                if cap > 0 and not visited[v]:
                    visited[v] = True
                    queue.append(v)

        # partition_s: reachable, partition_t: unreachable
        partition_s = {i for i in range(self.V) if visited[i]}
        partition_t = {i for i in range(self.V) if not visited[i]}

        # identify cut edges (from s-set to t-set in original graph)
        cut_edges = []
        for u in partition_s:
            if u in self.graph:
                for v, cap in self.graph[u].items():
                    if v in partition_t and cap > 0:
                        cut_edges.append((u, v))

        return max_flow, (partition_s, partition_t), cut_edges
