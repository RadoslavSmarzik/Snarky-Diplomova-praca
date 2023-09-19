from collections import deque
from functions_graph import *


# Trieda pre 2faktor
class TwoFactor():

    def __init__(self, c1, c2):
        self.cycle1 = c1
        self.cycle2 = c2

    def format_string(self):
        s = ""
        for i in range(len(self.cycle1)):
            s+=str(self.cycle1[i])
            if i < len(self.cycle1) - 1:
                s += " "
        s += '\n'
        for i in range(len(self.cycle2)):
            s += str(self.cycle2[i])
            if i < len(self.cycle2) - 1:
                s += " "
        s += '\n'
        return s

# Trieda pre hranu
class Edge:

    def __init__(self, u, v):
        self.u = u
        self.v = v

# Trieda pre graf
class Graph:

    def __init__(self, number_of_vertcies = None, adjacency_list = None):
        self.number_of_verticies = number_of_vertcies
        self.adjacency_list = adjacency_list
        self.twoFactors = []
        # pole obsahujuce vsetky cykly dlzky 5 v grafe
        self.cycles_of_5 = []
        self.selected_2factor = None

    def reset_graph(self):
        self.number_of_verticies = None
        self.adjacency_list = None
        self.twoFactors.clear()
        self.cycles_of_5.clear()
        self.selected_2factor = None

    def create_graph_from_file(self, filename):
        self.create_adjacency_list_from_file(filename)

    def create_adjacency_list_from_file(self, filename):
        f = open(filename, "r")
        first_row = f.readline()
        self.number_of_verticies = int(first_row)
        self.adjacency_list = []

        for i in range(self.number_of_verticies):
            three_verticies = f.readline().split()
            three_verticies_int = []
            for vertex in three_verticies:
                three_verticies_int.append(int(vertex))
            self.adjacency_list.append(three_verticies_int)
        f.close()

    # mame hrany e1, e2, f
    # e1 = e1_u e1_v
    # e2 = e2_u e2_v
    # f = f_u f_v
    # f_u_1 je jeden susedn f_u
    # f_u_2 je druhy sused f_u
    def do_dot_product(self, G2, e1_u, e1_v, e2_u, e2_v, f, f_u_1, f_u_2, f_v_1, f_v_2):
        adj_g1 = copy.deepcopy(self.adjacency_list)
        adj_g2 = copy.deepcopy(G2.adjacency_list)

        cut_edge_from_list(e1_u, e1_v, adj_g1)
        cut_edge_from_list(e2_u, e2_v, adj_g1)

        # upravime ocislovanie susedov hrany f, podla toho ake vrcholy sa z G2 odstarnuju
        f_u_1 = get_number_of_vertex_after_deleting(f_u_1, f.u, f.v)
        f_u_2 = get_number_of_vertex_after_deleting(f_u_2, f.u, f.v)
        f_v_1 = get_number_of_vertex_after_deleting(f_v_1, f.u, f.v)
        f_v_2 = get_number_of_vertex_after_deleting(f_v_2, f.u, f.v)

        # odstranujeme v poradi najprv vacsie cislo vrchola
        adj_g2 = delete_2_verticies_from_adj(adj_g2, f.u, f.v)

        # upravime ocislovanie druheho adjacency listu tak, ze ho posunieme o pocet vrcholov prveho
        adj_g2 = renumber_adj_list_by_shift(adj_g2, len(adj_g1))

        # musime aj free vrcholom, ktore budeme pripajat upravit ocislovanie
        f_u_1 = f_u_1 + len(adj_g1)
        f_u_2 = f_u_2 + len(adj_g1)
        f_v_1 = f_v_1 + len(adj_g1)
        f_v_2 = f_v_2 + len(adj_g1)

        # spojim adj listy
        result_ajd = adj_g1 + adj_g2

        # e1_u + f_u_1
        result_ajd[e1_u].append(f_u_1)
        result_ajd[f_u_1].append(e1_u)

        # e1_v + f_u_2
        result_ajd[e1_v].append(f_u_2)
        result_ajd[f_u_2].append(e1_v)

        # e2_u + f_v_1
        result_ajd[e2_u].append(f_v_1)
        result_ajd[f_v_1].append(e2_u)

        # e2_v + f_v_2
        result_ajd[e2_v].append(f_v_2)
        result_ajd[f_v_2].append(e2_v)

        return Graph(len(result_ajd), result_ajd)

    # pekne naformatovany zapis grafu
    def format_string(self):
        s = str(self.number_of_verticies) + "\n"
        for list in self.adjacency_list:
            row = ""
            for v in list:
                row += str(v) + " "
            s += row
            s += "\n"
        return s

    def adjacency_list_string(self):
        s = ""
        for i in range(len(self.adjacency_list)):
            s += str(i) +":"
            for v in self.adjacency_list[i]:
                s += " " + str(v)
            s += "\n"
        return s

    def get_neighbours_of_vertex(self, vertex):
        return copy.deepcopy(self.adjacency_list[vertex])

    ####################################### STAR PRODUCT ######################################3

    # metoda hlada 5-cykly v grafe a vrati ich pocet
    def find_5_cycles(self, k=5):
        self.n = len(self.adjacency_list)
        self.create_matrix()
        graph = self.matrix
        marked = [False] * self.n
        count = 0
        for i in range(self.n - (k - 1)):
            count = self.DFS(graph, marked, k - 1, i, i, count, [i])
            marked[i] = True

        return int(count / 2)

    # prehladavanie grafu, ktore hlada 5cykly
    def DFS(self, graph, marked, k, vert, start, count, path):
        marked[vert] = True
        if k == 0:
            marked[vert] = False
            if graph[vert][start] == 1:
                count = count + 1
                if not self.cycle_is_in_cycles_5(path):
                    self.cycles_of_5.append(path)
                return count
            else:
                return count

        for i in range(self.n):
            if marked[i] == False and graph[vert][i] == 1:
                next_path = path[:]
                next_path.append(i)
                count = self.DFS(graph, marked, k - 1, i, start, count, next_path)

        marked[vert] = False
        return count

    # pomocna funkcia, ktora zistuje ci pole b obsahuje vsetky prvky ako pole a
    def arrays_have_same_memebers(self,a, b):
        if len(a) != len(b):
            return False
        for element in a:
            if not element in b:
                return False
        return True

    # pomocna funkcia, ktora overuje ci dany 5-cyklus uz mame poznaceny
    def cycle_is_in_cycles_5(self,p):
        global paths
        for cycle in self.cycles_of_5:
            if self.arrays_have_same_memebers(p, cycle):
                return True
        return False

    # funkcia ktora vytvori graf ako maticu
    def create_matrix(self):
        n = len(self.adjacency_list)
        self.matrix = [[0 for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in self.adjacency_list[i]:
                self.matrix[i][j] = 1

    # metoda, ktora vytvori star product na zaklade zvolenych 5 cyklov a 2faktorov
    def doStarProduct(self, G2, g1_5cycle, g2_5cycle, g1_twoFactor, g2_twoFactor, g1_reverse_cycle, g2_reverse_cycle):
        g1_adj = copy.deepcopy(self.adjacency_list)
        g2_adj = copy.deepcopy(G2.adjacency_list)

        # najdem index zacinajuceho vrchola, ktory je z priecky
        g1_index_of_spoke_vertex = self.find_index_of_spoke_vertex(g1_5cycle, g1_twoFactor.cycle1, g1_twoFactor.cycle2)
        g2_index_of_spoke_vertex = self.find_index_of_spoke_vertex(g2_5cycle, g2_twoFactor.cycle1, g2_twoFactor.cycle2)

        # upravim pole aby prieckovy vrchol bol prvy
        g1_5cycle = self.shift_array(g1_5cycle, g1_index_of_spoke_vertex)
        g2_5cycle = self.shift_array(g2_5cycle, g2_index_of_spoke_vertex)

        # najdem susedov cyklov
        free_of_g1_5cycle = self.get_neighbours_of_cycle(self.adjacency_list, g1_5cycle)
        free_of_g2_5cycle = self.get_neighbours_of_cycle(G2.adjacency_list, g2_5cycle)

        # vyhod z adjacency listov 5 cykly
        g1_adj = self.delete_verticies_from_adj(g1_5cycle, g1_adj)
        g2_adj = self.delete_verticies_from_adj(g2_5cycle, g2_adj)

        # uprav volne vrcholy podla toho co vlastne odstranujem
        free_of_g1_5cycle = self.renumber_verticies_after_deleting(free_of_g1_5cycle, g1_5cycle)
        free_of_g2_5cycle = self.renumber_verticies_after_deleting(free_of_g2_5cycle, g2_5cycle)

        # posun vsetko v adj2 o velkost adj1
        g2_adj = renumber_adj_list_by_shift(g2_adj, len(g1_adj))

        # posun oznacenie volnych vrcholov a ovelkost adj1
        free_of_g2_5cycle = self.renumber_array_by_shift(free_of_g2_5cycle, len(g1_adj))

        # ideme spajat
        g3_adj = g1_adj + g2_adj

        # tu sa da pohrat, ktorym smerom pojdeme tie free cykly ci zlava doprava alebo naopak
        # reversnem poradie volnych vrcholov g1, ak je TRUE
        if g1_reverse_cycle:
            free_of_g1_5cycle = self.reverse_order_of_array_from_index_1(free_of_g1_5cycle)

        # reversnem poradie volnych vrcholov g2, ak je TRUE
        if g2_reverse_cycle:
            free_of_g2_5cycle = self.reverse_order_of_array_from_index_1(free_of_g2_5cycle)

        # spoj volne z g1 s g2
        for i in range(len(free_of_g1_5cycle)):
            g3_adj[free_of_g1_5cycle[i]].append(free_of_g2_5cycle[2 * i % 5])
            g3_adj[free_of_g2_5cycle[2 * i % 5]].append(free_of_g1_5cycle[i])

        G3 = Graph(len(g3_adj), g3_adj)
        return G3

    def reverse_order_of_array_from_index_1(self, array):
        new_array = [array[0]]
        array.pop(0)
        array.reverse()
        new_array.extend(array)
        return new_array

    def renumber_array_by_shift(self, array, shift):
        for i in range(len(array)):
            array[i] = array[i] + shift
        return array

    def renumber_verticies_after_deleting(self, free_array, delete_array):
        delete_array.sort(reverse=True)
        new_array = []
        for element in free_array:
            new_element = element
            for i in range(len(delete_array)):
                if element > delete_array[i]:
                    new_element = new_element - 1
            new_array.append(new_element)
        return new_array

    def delete_verticies_from_adj(self, delete_array, adj_list):
        delete_array.sort(reverse=True)
        for element in delete_array:
            delete_vertex_from_adj_list(element, adj_list)
        return adj_list

    # najde index na ktorom je vrchol z priecky
    def find_index_of_spoke_vertex(self, cycle_of_5, cycle1, cycle2):
        for i in range(len(cycle_of_5)):
            vertex = cycle_of_5[i]
            vertex_before = cycle_of_5[i-1] if i > 0 else cycle_of_5[len(cycle_of_5) - 1]
            vertex_after = cycle_of_5[i+1] if i < len(cycle_of_5)-1 else cycle_of_5[0]
            if (vertex in cycle1 and vertex_before in cycle1 and vertex_after in cycle1) or (vertex in cycle2 and vertex_before in cycle2 and vertex_after in cycle2):
                return i

    # shifne pole dolava tak, ze prvy bude vrchol na indexe shift
    def shift_array(self, array, shift):
        myarray = deque(array)
        myarray.rotate(-shift)  # rotate left
        return list(myarray)

    # metoda vrati pole volnych susedov cyklu
    def get_neighbours_of_cycle(self, adjacency_list, cycle):
        new_array = []
        for element in cycle:
            for i in range(3):
                if not adjacency_list[element][i] in cycle:
                    new_array.append(adjacency_list[element][i])
        return new_array

    # funkcia vrati unfix vrchol, pre vertex a fix
    # vychadza z toho, ze vertex ma 3 susedov, pricom dvaja z nich musia byt vertex2 a fix
    # cize unfix bude treti
    def get_unfix(self, vertex, fix, vertex2):
        vertex_neighbours = get_neighbous_of_vertex_without_vertex2(self, vertex, vertex2)
        vertex_neighbours.remove(fix)
        return vertex_neighbours.pop()

    # involucny symetricky 4-sucin - konstrukcia 1
    # fix_1 a fix_2 je hrana medzi, ktoru budeme vkladat pevny bod
    def inv_sym_4_sucin_konstrukcia_1(self, vertex1, vertex2, fix_1, fix_2):
        # vertex1 a vertex2 musia tvorit priecku
        # fix_1 a fix_2 budu tvorit hranu medzi ktoru sa vlozi pevny bod
        # vertex1 susedi s vertex 2 - tuto hranu sme odstranovali
        # vertex1 susedi s fix_1
        # vertex1 susedi s unfix_1


        adj_list = copy.deepcopy(self.adjacency_list)

        unfix_1 = self.get_unfix(vertex1, fix_1, vertex2)
        unfix_2 = self.get_unfix(vertex2, fix_2, vertex1)

        # odstranim vrcholy, ktore tvorili priecku zo zoznamu susedov
        adj_list = delete_2_verticies_from_adj(adj_list, vertex1, vertex2)

        # spavime druhu kopiu adj listu a posunieme cisla na spravne miesto
        adj_list2 = copy.deepcopy(adj_list)
        adj_list2 = renumber_adj_list_by_shift(adj_list2, len(adj_list))

        # spojim listy
        adj_list_final = adj_list + adj_list2

        # upravime na spravne ocislovanie
        fix_1 = get_number_of_vertex_after_deleting(fix_1, vertex1, vertex2)
        fix_2 = get_number_of_vertex_after_deleting(fix_2, vertex1, vertex2)
        unfix_1 = get_number_of_vertex_after_deleting(unfix_1, vertex1, vertex2)
        unfix_2 = get_number_of_vertex_after_deleting(unfix_2, vertex1, vertex2)

        # vytvorim hrany (odkomentovane su hrany, ktore su zbytocne, lebo sa medzi ne vlozi pevny bod)
        # adj_list_final[fix1].append(fix2 + len(adj_list))
        adj_list_final[unfix_1].append(unfix_2 + len(adj_list))
        # adj_list_final[fix2].append(fix1 + len(adj_list))
        adj_list_final[unfix_2].append(unfix_1 + len(adj_list))


        # adj_list_final[fix2 + len(adj_list)].append(fix1)
        adj_list_final[unfix_2 + len(adj_list)].append(unfix_1)
        # adj_list_final[fix1 + len(adj_list)].append(fix2)
        adj_list_final[unfix_1 + len(adj_list)].append(unfix_2)

        # vlozenie pevneho bodu
        p1 = len(adj_list_final)
        p2 = p1 + 1

        adj_list_final.append([p2])
        adj_list_final.append([p1])

        # p1 vlozim medzi hranovy
        adj_list_final[p1].append(fix_1)
        adj_list_final[p1].append(fix_2 + len(adj_list))

        adj_list_final[fix_1].append(p1)
        adj_list_final[fix_2 + len(adj_list)].append(p1)

        # p2 vlozim medzi hranovy
        adj_list_final[p2].append(fix_2)
        adj_list_final[p2].append(fix_1 + len(adj_list))

        adj_list_final[fix_2].append(p2)
        adj_list_final[fix_1 + len(adj_list)].append(p2)


        G3 = Graph(len(adj_list_final), adj_list_final)

        return G3

    # KONSTRUKCIA 2

    def is_spoke_edge(self, v1, v2, two_factor):
        if (v1 in two_factor.cycle1 and v2 in two_factor.cycle2) or (v1 in two_factor.cycle2 and v2 in two_factor.cycle1):
            return True
        return False

    def initializeFreeElements(self,number):
        array = []
        for i in range(number):
            array.append(i)
        return array

    def areNeighboars(self,vertex1, vertex2):
        return vertex1 in self.adjacency_list[vertex2]

    def getNeighboarIndexFromPermutaion(self, vertex, permutaion):
        for i in range(len(permutaion)):
            if self.areNeighboars(vertex, permutaion[i]):
                return i

    def is_involution(self, permutation):
        for i in permutation:
            if len(i) > 2:
                return False
        return True

    def create_permutation(self, cycle1, cycle2):
        permutation = []
        free_numbers = self.initializeFreeElements(int(self.number_of_verticies / 2))

        while len(free_numbers) > 0:
            cycle_of_permuation = []
            element = min(free_numbers)
            while not element in cycle_of_permuation:
                cycle_of_permuation.append(element)
                free_numbers.remove(element)
                element = self.getNeighboarIndexFromPermutaion(cycle1[element], cycle2)
            permutation.append(cycle_of_permuation)

        return permutation

    # pre two factor a mozny pevny bod skusim najst involuciu
    def find_involution_for_two_factor_and_fix_point(self, vertex_in_c1, vertex_in_c2, two_factor):
        cycle1 = copy.deepcopy(two_factor.cycle1)
        cycle2 = copy.deepcopy(two_factor.cycle2)

        cycle1 = self.shift_array(cycle1, cycle1.index(vertex_in_c1))
        cycle2 = self.shift_array(cycle2, cycle2.index(vertex_in_c2))
        cycle2_reverse = self.reverse_order_of_array_from_index_1(copy.deepcopy(cycle2))

        # vytvorim permutaciu na zaklede vstupov cycle1 a cycle2
        perm1 = self.create_permutation(cycle1, cycle2)

        if self.is_involution(perm1):
            return(cycle1, cycle2)

        # vytvorim permutaciu na zaklede vstupov cycle1 a otoceneho cycle2
        perm2 = self.create_permutation(cycle1, cycle2_reverse)
        if self.is_involution(perm2):
            return (cycle1, cycle2_reverse)

        return None

    # pre two factor a mozny pevny bod skusim najst involuciu
    def find_all_involutions_for_two_factor_and_fix_point(self, vertex_in_c1, vertex_in_c2, two_factor):
        array = []
        cycle1 = copy.deepcopy(two_factor.cycle1)
        cycle2 = copy.deepcopy(two_factor.cycle2)

        cycle1 = self.shift_array(cycle1, cycle1.index(vertex_in_c1))
        cycle2 = self.shift_array(cycle2, cycle2.index(vertex_in_c2))
        cycle2_reverse = self.reverse_order_of_array_from_index_1(copy.deepcopy(cycle2))

        # vytvorim permutaciu na zaklede vstupov cycle1 a cycle2
        perm1 = self.create_permutation(cycle1, cycle2)

        if self.is_involution(perm1):
            array.append((cycle1, cycle2))

        # vytvorim permutaciu na zaklede vstupov cycle1 a otoceneho cycle2
        perm2 = self.create_permutation(cycle1, cycle2_reverse)
        if self.is_involution(perm2):
            array.append((cycle1, cycle2_reverse))

        if len(array) > 0:
            return array

        return None

    def find_all_involutions_for_twoFactor(self, two_factor):
        involutions_array = []
        for i in range(len(self.adjacency_list)):
            for j in range(len(self.adjacency_list[i])):
                if i < self.adjacency_list[i][j]:   # zabranenie duplicitam
                    v1 = i
                    v2 = self.adjacency_list[i][j]
                    if self.is_spoke_edge(v1, v2, two_factor):
                        if v1 in two_factor.cycle1:
                            involution = self.find_all_involutions_for_two_factor_and_fix_point(v1, v2, two_factor)
                        else:
                            involution = self.find_all_involutions_for_two_factor_and_fix_point(v2, v1, two_factor)
                        if involution is not None:
                            involutions_array.extend(involution)
        return involutions_array

    # pre zvoleny 2 factor skusi najst involuciu, ak nenajde tak vrati None
    def get_first_involution_for_2factor(self, two_factor):
        # prejdeme vsetky mozne variacie na pevny bod, ktore su pri two_factore, cize vsetky priecky
        for i in range(len(self.adjacency_list)):
            for j in range(len(self.adjacency_list[i])):
                v1 = i
                v2 = self.adjacency_list[i][j]
                if self.is_spoke_edge(v1, v2, two_factor):
                    if v1 in two_factor.cycle1:
                        involution = self.find_involution_for_two_factor_and_fix_point(v1, v2, two_factor)
                    else:
                        involution = self.find_involution_for_two_factor_and_fix_point(v2, v1, two_factor)
                    if involution is not None:
                        return involution
        return None

    # g1_fix_point_1 a g1_fix_point_2 v grafe G1 tvoria hranu, ktora je pevny bod
    def inv_sym_4_konstrukcia_2(self, G2, g1_fix_1, g2_fix_1, g1_fix_2, g2_fix_2,
                                g1_unfix_1, g2_unfix_1, g1_unfix_2, g2_unfix_2,
                                g1_fix_point_1, g1_fix_point_2, g2_fix_point_1, g2_fix_point_2):
        # spojime g1_fix_1 a g2_fix_1
        # spojime g1_unfix_1 a g2_unfix_1

        g1_adj = copy.deepcopy(self.adjacency_list)
        g2_adj = copy.deepcopy(G2.adjacency_list)

        # odstranujem pevne body z g1 aj g2
        g1_adj = delete_2_verticies_from_adj(g1_adj, g1_fix_point_1, g1_fix_point_2)

        g2_adj = delete_2_verticies_from_adj(g2_adj, g2_fix_point_1, g2_fix_point_2)

        # upravujem oznacenia bodov, ktore budem spajat
        g1_fix_1 = get_number_of_vertex_after_deleting(g1_fix_1, g1_fix_point_1, g1_fix_point_2)
        g2_fix_1 = get_number_of_vertex_after_deleting(g2_fix_1, g2_fix_point_1, g2_fix_point_2)
        g1_fix_2 = get_number_of_vertex_after_deleting(g1_fix_2, g1_fix_point_1, g1_fix_point_2)
        g2_fix_2 = get_number_of_vertex_after_deleting(g2_fix_2, g2_fix_point_1, g2_fix_point_2)

        g1_unfix_1 = get_number_of_vertex_after_deleting(g1_unfix_1, g1_fix_point_1, g1_fix_point_2)
        g2_unfix_1 = get_number_of_vertex_after_deleting(g2_unfix_1, g2_fix_point_1, g2_fix_point_2)
        g1_unfix_2 = get_number_of_vertex_after_deleting(g1_unfix_2, g1_fix_point_1, g1_fix_point_2)
        g2_unfix_2 = get_number_of_vertex_after_deleting(g2_unfix_2, g2_fix_point_1, g2_fix_point_2)

        # posuniem vrcholy g2 o velkost g1
        g2_adj = renumber_adj_list_by_shift(g2_adj, len(g1_adj))

        # spojim listy
        adj_list_final = g1_adj + g2_adj

        # vytvorim hrany
        # adj_list_final[hranovy1].append(hranovy2 + len(adj_list))
        adj_list_final[g1_unfix_1].append(g2_unfix_1 + len(g1_adj))
        # adj_list_final[hranovy2].append(hranovy1 + len(adj_list))
        adj_list_final[g1_unfix_2].append(g2_unfix_2 + len(g1_adj))

        # adj_list_final[hranovy2 + len(adj_list)].append(hranovy1)
        adj_list_final[g2_unfix_1 + len(g1_adj)].append(g1_unfix_1)
        # adj_list_final[hranovy1 + len(adj_list)].append(hranovy2)
        adj_list_final[g2_unfix_2 + len(g1_adj)].append(g1_unfix_2)

        # vlozenie pevneho bodu
        p1 = len(adj_list_final)
        p2 = p1 + 1

        adj_list_final.append([p2])
        adj_list_final.append([p1])

        # p1 vlozim medzi hranovy
        adj_list_final[p1].append(g1_fix_1)
        adj_list_final[p1].append(g2_fix_1 + len(g1_adj))

        adj_list_final[g1_fix_1].append(p1)
        adj_list_final[g2_fix_1 + len(g1_adj)].append(p1)

        # p2 vlozim medzi hranovy
        adj_list_final[p2].append(g1_fix_2)
        adj_list_final[p2].append(g2_fix_2 + len(g1_adj))

        adj_list_final[g1_fix_2].append(p2)
        adj_list_final[g2_fix_2 + len(g1_adj)].append(p2)

        G3 = Graph(len(adj_list_final), adj_list_final)

        return G3

    # dipol konstrukcia 1
    # g1_vertex_1 a g1_vertex_2 su vybrana hrana, g1_zodpovedajuc_1 a g1_zodpovedajuci_2 je zodpovedajuca hrana
    def dipol_konstrukcia_1(self, g1_vertex_1, g1_zodpovedajuc_1, g1_vertex_2, g1_zodpovedajuci_2,
                            dipol_adj_original, dipol_red_A, dipol_red_B, dipol_blue_A, dipol_blue_B):

        adj_list = copy.deepcopy(self.adjacency_list)
        dipol_adj = copy.deepcopy(dipol_adj_original)

        # rozrem hrany
        cut_edge_from_list(g1_vertex_1, g1_vertex_2, adj_list)
        cut_edge_from_list(g1_zodpovedajuc_1, g1_zodpovedajuci_2, adj_list)

        # posuniem vrcholy v dipol_adj
        dipol_adj = renumber_adj_list_by_shift(dipol_adj, len(adj_list))

        # vertex1 spojim s dipol_red_A
        adj_list[g1_vertex_1].append(len(adj_list) + dipol_red_A)
        dipol_adj[dipol_red_A].append(g1_vertex_1)

        # musim teda zodpovedajuci1 spojit s dipol_blue_A
        adj_list[g1_zodpovedajuc_1].append(len(adj_list) + dipol_blue_A)
        dipol_adj[dipol_blue_A].append(g1_zodpovedajuc_1)

        # musim teda vertex2 spojit s dipol_red_B
        adj_list[g1_vertex_2].append(len(adj_list) + dipol_red_B)
        dipol_adj[dipol_red_B].append(g1_vertex_2)

        # musim teda zodpovedajuci2 spojit s dipol_blue_B
        adj_list[g1_zodpovedajuci_2].append(len(adj_list) + dipol_blue_B)
        dipol_adj[dipol_blue_B].append(g1_zodpovedajuci_2)

        final_adj = adj_list + dipol_adj
        G3 = Graph(len(final_adj), final_adj)
        return G3

    # vytvor dipol

    def create_dipol(self, blue_cycle, red_cycle):
        adj_list = copy.deepcopy(self.adjacency_list)

        fix_point_1 = blue_cycle[0]
        fix_point_2 = red_cycle[0]

        # zistim zvysnych susedov pre pevny_1 aj pevny_2
        neighbours_fix_point_1 = get_neighbous_of_vertex_without_vertex2(self, fix_point_1, fix_point_2)
        neighbours_fix_point_2 = get_neighbous_of_vertex_without_vertex2(self, fix_point_2, fix_point_1)

        # odstran pevny bod (pozor na poradie)
        delete_2_verticies_from_adj(adj_list, fix_point_1, fix_point_2)

        # blue_A je oznaceny vrchol, ktory zodpoveda vrcholu red_A
        # blue_B je oznaceny vrchol, ktory zodpoveda vrcholu red_B
        # to sa bude hodit pri vkladani dipolu v buducnosti

        if neighbours_fix_point_1[0] in blue_cycle:
            blue_neighbours = neighbours_fix_point_1
        elif neighbours_fix_point_2[0] in blue_cycle:
            blue_neighbours = neighbours_fix_point_2

        dipol_adj = adj_list
        blue_A = blue_neighbours[0]
        blue_B = blue_neighbours[1]

        red_A = find_corresponding_vertex(blue_A, blue_cycle, red_cycle)
        red_B = find_corresponding_vertex(blue_B, blue_cycle, red_cycle)

        # vratim adjacency list dipolu a volne vrcholy
        # pozor blue_A, blue_B, red_A, red_B su hodnoty vrcholov este ked tam bol pevny bod
        # pri praci s dipolom tieto hodnoty musime aktualizovat
        return [dipol_adj, blue_A, blue_B, red_A, red_B]


    # dipol 2 konstrukcia
    def dipol_konstrukcia_2(self, g1_vertex_1, g1_zodpovedajuci_1, g1_vertex_2, g1_zodpovedajuci_2,
                            g1_vertex_3, g1_zodpovedajuci_3, g1_vertex_4, g1_zodpovedajuci_4,
                            G2, dipol_red_A, dipol_red_B, dipol_blue_A, dipol_blue_B, fix_point_1, fix_point_2):

        adj_list = copy.deepcopy(self.adjacency_list)

        adj_list_2 = copy.deepcopy(G2.adjacency_list)

        # z G2 odstranim pevny bod, cize vytvorim dipol
        adj_list_2 = delete_2_verticies_from_adj(adj_list_2, fix_point_1, fix_point_2)

        dipol_adj = copy.deepcopy(adj_list_2)
        dipol_adj_2 = copy.deepcopy(adj_list_2)

        # rozrem hrany
        cut_edge_from_list(g1_vertex_1, g1_vertex_2, adj_list)
        cut_edge_from_list(g1_zodpovedajuci_1, g1_zodpovedajuci_2, adj_list)
        cut_edge_from_list(g1_vertex_3, g1_vertex_4, adj_list)
        cut_edge_from_list(g1_zodpovedajuci_3, g1_zodpovedajuci_4, adj_list)

        # posuniem vrcholy v dipol_adj a dipol_adj_2
        dipol_adj = renumber_adj_list_by_shift(dipol_adj, len(adj_list))
        dipol_adj_2 = renumber_adj_list_by_shift(dipol_adj_2, len(adj_list) + len(dipol_adj))

        # vertex1 spojim s dipol_red_A - 1
        adj_list[g1_vertex_1].append(len(adj_list) + dipol_red_A)
        dipol_adj[dipol_red_A].append(g1_vertex_1)

        # vertex2 s dipol_red_B - 1
        adj_list[g1_vertex_2].append(len(adj_list) + dipol_red_B)
        dipol_adj[dipol_red_B].append(g1_vertex_2)

        # zodpovedajuci3 s dipol_blue_A - 1
        adj_list[g1_zodpovedajuci_3].append(len(adj_list) + dipol_blue_A)
        dipol_adj[dipol_blue_A].append(g1_zodpovedajuci_3)

        # zodpovedajuci4 s dipol_blue_B - 1
        adj_list[g1_zodpovedajuci_4].append(len(adj_list) + dipol_blue_B)
        dipol_adj[dipol_blue_B].append(g1_zodpovedajuci_4)

        # zodpovedajuci_1 spojim s dipol_red_A - 2
        adj_list[g1_zodpovedajuci_1].append(len(adj_list) + dipol_red_A + len(dipol_adj))
        dipol_adj_2[dipol_red_A].append(g1_zodpovedajuci_1)

        # zodpovedajuci_2 s dipol_red_B - 2
        adj_list[g1_zodpovedajuci_2].append(len(adj_list) + dipol_red_B + len(dipol_adj))
        dipol_adj_2[dipol_red_B].append(g1_zodpovedajuci_2)

        # vertex_3 s dipol_blue_A - 2
        adj_list[g1_vertex_3].append(len(adj_list) + dipol_blue_A + len(dipol_adj))
        dipol_adj_2[dipol_blue_A].append(g1_vertex_3)

        # vertex_4 s dipol_blue_B - 2
        adj_list[g1_vertex_4].append(len(adj_list) + dipol_blue_B + len(dipol_adj))
        dipol_adj_2[dipol_blue_B].append(g1_vertex_4)

        final_adj = adj_list + dipol_adj + dipol_adj_2
        G3 = Graph(len(final_adj), final_adj)
        return G3


