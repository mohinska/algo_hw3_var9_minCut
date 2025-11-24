import networkx as nx
import timeit
import random
from min_cut_solver import MinCutSolver

def verify_correctness():
    print("--- Test ---")
    solver = MinCutSolver(6)
    edges = [
        (0, 1, 16), (0, 2, 13),
        (1, 2, 10), (1, 3, 12),
        (2, 1, 4), (2, 4, 14),
        (3, 2, 9), (3, 5, 20),
        (4, 3, 7), (4, 5, 4)
    ]

    G_nx = nx.DiGraph()
    for u, v, w in edges:
        solver.add_edge(u, v, w)
        G_nx.add_edge(u, v, capacity=w)

    # Custom Result
    my_flow, my_partition, my_edges = solver.solve(0, 5)
    my_cut_val = sum(solver.graph[u][v] for u, v in my_edges)

    # NetworkX Result
    nx_cut_val, nx_partition = nx.minimum_cut(G_nx, 0, 5)

    print(f"Custom Flow: {my_flow}, Custom Cut Capacity: {my_cut_val}")
    print(f"NetworkX Cut Capacity: {nx_cut_val}")

    if my_cut_val == nx_cut_val:
        print("SUCCESS: Results match.")
    else:
        print("FAILURE: Mismatch found.")

def benchmark():
    print("\n--- Benchmark ---")
    sizes = [(20, 60), (50, 250), (100, 1000), (200, 4000), (500, 12500)]

    for V, E in sizes:
        # generate random graph data
        edges = []
        for _ in range(E):
            u = random.randint(0, V-1)
            v = random.randint(0, V-1)
            if u!= v:
                cap = random.randint(1, 20)
                edges.append((u, v, cap))

        # setup custom
        solver = MinCutSolver(V)
        for u, v, w in edges:
            solver.add_edge(u, v, w)

        G_nx = nx.DiGraph()
        G_nx.add_weighted_edges_from(edges, weight='capacity')

        # time custom
        t_custom = timeit.timeit(lambda: solver.solve(0, V-1), number=10) / 10

        # time nx
        t_nx = timeit.timeit(lambda: nx.minimum_cut(G_nx, 0, V-1, flow_func=nx.algorithms.flow.edmonds_karp), number=10) / 10

        print(f"Size V={V}, E={E} | Custom: {t_custom:.5f}s | NX: {t_nx:.5f}s")

if __name__ == "__main__":
    verify_correctness()
    benchmark()
