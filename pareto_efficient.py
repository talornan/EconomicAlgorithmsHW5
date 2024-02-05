import math
import networkx as nx


def is_pareto_efficient(valuations: list[list[float]], allocation: list[list[float]]) -> bool:
    """
    Check if the given allocation is Pareto efficient using the barter graph approach.

    Parameters:
    - valuations (list[list[float]]): List of lists representing the valuations of each player.
    - allocation (list[list[float]]): List of lists representing the allocation of resources to each player.

    Returns:
    - bool: True if the allocation is Pareto efficient, False otherwise.
        """
    graph = build_graph(valuations, allocation)
    return not has_negative_cycle(graph)


def has_negative_cycle(graph: nx.Graph) -> bool:
    """
    Check if the graph has a negative cycle by transforming edge weights to their logarithm.

    Parameters:
    - graph (nx.Graph): The input graph.

    Returns:
    - bool: False if a negative cycle is found, True otherwise.
    """
    # Trying to find negative cycle with builtin function
    try:
        nx.find_negative_cycle(graph, 0)
        return True  # Negative cycle found
    except nx.NetworkXError:
        return False  # No negative cycle found


def build_graph(valuations: list[list[float]], allocation: list[list[float]]) -> nx.DiGraph:
    """
    Build a directed graph where each player has an edge to every other player with weights calculated by log transformation.

    Parameters:
    - valuations (list[list[float]]): List of lists representing the valuations of each player.
    - allocation (list[list[float]]): List of lists representing the allocation of resources to each player.

    Returns:
    - nx.DiGraph: Directed graph representing the barter graph.
    """
    G = nx.DiGraph()
    player_num = len(valuations)
    G.add_nodes_from(range(player_num))

    for i in range(player_num):
        for j in range(player_num):
            if i != j:
                selected_weight = math.log10(calculate_min_ratio(i, j, valuations, allocation))
                G.add_edge(i, j, weight=selected_weight)

    return G


def calculate_min_ratio(i, j, valuations, allocation):
    """
    Calculate the minimum ratio of values above market price between players i and j for a given allocation.

    Parameters:
    - i (int): Index of player i.
    - j (int): Index of player j.
    - valuations (list[list[float]]): List of lists representing the valuations of each player.
    - allocation (list[list[float]]): List of lists representing the allocation of resources to each player.

    Returns:
    - float: The minimum ratio of values above market price.
    """
    non_zero_ratios = [(valuations[i][k] * allocation[i][k]) / (valuations[j][k] * allocation[j][k])
                       for k in range(len(allocation[i])) if allocation[i][k] != 0 and allocation[j][k] != 0]

    return min(non_zero_ratios, default=float('inf'))


# Additional tests
def test_is_pareto_efficient():
    # Example 1: Pareto efficient allocation
    valuations1 = [[10, 20, 30, 40], [40, 30, 20, 10]]
    allocation1 = [[0, 0.7, 1, 1], [1, 0.3, 0, 0]]
    result1 = is_pareto_efficient(valuations1, allocation1)
    print("Test 1:", result1)
    assert result1 == True

    # Example 2: Not Pareto efficient allocation
    valuations2 = [[10, 15, 20], [30, 40, 50]]
    allocation2 = [[0.7, 0.3, 0], [0.5, 0.5, 0]]
    result2 = is_pareto_efficient(valuations2, allocation2)
    print("Test 2:", result2)
    assert result2 == False

    # Example 3: Not Pareto efficient allocation
    valuations3 = [[10, 20], [20, 10]]
    allocation3 = [[0.5, 0.5], [0.5, 0.5]]
    result3 = is_pareto_efficient(valuations3, allocation3)
    print("Test 3:", result3)
    assert result3 == False

    # Example 4: Pareto efficient allocation
    valuations4 = [[10, 20], [30, 40]]
    allocation4 = [[1, 0], [0, 1]]
    result4 = is_pareto_efficient(valuations4, allocation4)
    print("Test 4:", result4)
    assert result4 == True

    # Example 5: Pareto efficient allocation
    valuations5 = [[10, 20, 30], [30, 20, 10]]
    allocation5 = [[0.2, 0.8, 0], [0, 0, 1]]
    result5 = is_pareto_efficient(valuations5, allocation5)
    print("Test 5:", result5)
    assert result5 == True


test_is_pareto_efficient()
