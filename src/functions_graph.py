import copy
import networkx as nx

# vrati ako bude oznaceny vertex, po odstraneni deleted_vertex1 a deleted_vertex2
def get_number_of_vertex_after_deleting(vertex, deleted_vertex1, deleted_vertex2):
    new_vertex_number = vertex
    if vertex > deleted_vertex1:
        new_vertex_number = new_vertex_number - 1
    if vertex > deleted_vertex2:
        new_vertex_number = new_vertex_number - 1
    return new_vertex_number

# vrati susedov vertexu bez vrcholu remov_vertex
def get_neighbous_of_vertex_without_vertex2(graph, vertex, remove_vertex):
    neighbours = copy.deepcopy(graph.adjacency_list[vertex])
    neighbours.remove(remove_vertex)
    return neighbours

# Metoda vrati adjacency list s prerezanou hranou vertex1, vertex2
def cut_edge_from_list(vertex1, vertex2, adj_list):
    adj_list[vertex1].remove(vertex2)
    adj_list[vertex2].remove(vertex1)
    return adj_list

# Metoda z adjacency listu odstani vertex spravne, teda aj precisluje
def delete_vertex_from_adj_list(vertex, adj_list):
    # odstranovanie
    for list in adj_list:
        if vertex in list:
            list.remove(vertex)
    adj_list.pop(vertex)

    # precislovanie
    for list in adj_list:
        for i in range(len(list)):
            if list[i] > vertex:
                list[i] = list[i] - 1

def renumber_adj_list_by_shift(adj, shift):
    for list in adj:
        for i in range(len(list)):
            list[i] = list[i] + shift
    return adj

def get_neighbours_of_vertex(self, vertex):
    return copy.deepcopy(self.adjacency_list[vertex])

# z adj listu vymaze 2 vrcholy ale da pozor aby sme najprv odstranili ten vacsi
def delete_2_verticies_from_adj(adj, vertex1, vertex2):
    if vertex1 > vertex2:
        delete_vertex_from_adj_list(vertex1, adj)
        delete_vertex_from_adj_list(vertex2, adj)
    else:
        delete_vertex_from_adj_list(vertex2, adj)
        delete_vertex_from_adj_list(vertex1, adj)
    return adj

# metoda vyfiltuje pole grafov vzhladom na izomorfizmus
def isomorphism_filter_graphs(graphs):
    for i in range(len(graphs) - 1, -1, -1):
        g = graphs[i]
        graphs_without_g = copy.deepcopy(graphs)
        graphs_without_g.pop(i)
        if is_isomorphic_graph_in_array(g, graphs_without_g):
            graphs.remove(g)
    return graphs


# funkcia povie ci sa v poly nachadza nejaky graf izomorfny ku grafu graph
def is_isomorphic_graph_in_array(graph, array):
    for i in range(len(array)):
        if are_isomorphic(graph, array[i]):
            return True
    return False

# funkcia overi ci su 2 grafy izomorfne pomocou nx kniznice
def are_isomorphic(graph1, graph2):
    g1 = create_network_graph_object(graph1.adjacency_list)
    g2 = create_network_graph_object(graph2.adjacency_list)
    if nx.is_isomorphic(g1, g2):
        return True
    return False

# z adjlistu vytvori network graph object
def create_network_graph_object(adjlist):
    G = nx.Graph()
    for i in range(len(adjlist)):
        for j in range(len(adjlist[i])):
            G.add_edge(i, adjlist[i][j])
    return G

# najde zodpovedajuci vrchol
def find_corresponding_vertex(vertex, blue_cycle, red_cycle):
    if vertex in blue_cycle:
        index = blue_cycle.index(vertex)
        return red_cycle[index]

    elif vertex in red_cycle:
        index = red_cycle.index(vertex)
        return blue_cycle[index]