from functools import partial
from tkinter import messagebox
from functions import *
from functions_graph import *
from page import Page

# trieda pre vkladanie involucneho dipolu
class Page_dipol_1(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_selection_frame()
        bind_function_to_button(self.g1_button_add_2factors, partial(self.function_load_2factor_g1, self.G1, self.g1_combo_box, self.g1_array_of_labels))
        bind_function_to_button(self.g2_button_add_2factors, partial(self.function_load_2factor_g2, self.G2, self.g2_combo_box, self.g2_array_of_labels))
        self.selected_selection_lbl = None
        self.selected_edge_label = None
        bind_function_to_button(self.result_button, self.function_dipol_construction_1)
        bind_function_to_button(self.result_all_button, self.function_dipol_construction_1_all)

        self.create_inv_combo_boxes()
        self.g1_involutions_for_current_2factor = []
        self.g2_involutions_for_current_2factor = []

    def function_load_2factor_g1(self, graph, combo_box, array_of_labels):
        self.function_load_2factors_from_file(graph, combo_box, array_of_labels, filter_involution_2_factors=True)
        self.set_g1_red_and_blue_cycles(graph)

    def function_load_2factor_g2(self, graph, combo_box, array_of_labels):
        self.function_load_2factors_from_file(graph, combo_box, array_of_labels, filter_involution_2_factors=True)
        self.create_g2_dipol_and_set_cycles(graph)

    def create_g2_dipol_and_set_cycles(self, graph):
        if graph.selected_2factor is None:
            return
        self.g2_involutions_for_current_2factor = graph.find_all_involutions_for_twoFactor(graph.selected_2factor)
        self.combo_box_g2_inv["values"] = self.create_values_for_inv_combo_box(self.g2_involutions_for_current_2factor)
        self.combo_box_g2_inv.current(0)

        involution_2factor = self.g2_involutions_for_current_2factor[0]
        self.g2_blue_cycle = involution_2factor[0]
        self.g2_red_cycle = involution_2factor[1]
        self.create_dipol_from_G2()

    def create_dipol_from_G2(self):
        fix_point_1 = self.g2_blue_cycle[0]
        fix_point_2 = self.g2_red_cycle[0]
        dipol = self.G2.create_dipol(self.g2_blue_cycle, self.g2_red_cycle)

        self.dipol_adj = dipol[0]
        self.blue_A = dipol[1]
        self.blue_B = dipol[2]

        self.red_A = dipol[3]
        self.red_B = dipol[4]

        self.r_A.config(text="r_A:" + str(self.red_A))
        self.r_B.config(text="r_B:" + str(self.red_B))
        self.b_A.config(text="b_A:" + str(self.blue_A))
        self.b_B.config(text="b_B:" + str(self.blue_B))

        self.blue_A = get_number_of_vertex_after_deleting(self.blue_A, fix_point_1, fix_point_2)
        self.blue_B = get_number_of_vertex_after_deleting(self.blue_B, fix_point_1, fix_point_2)
        self.red_A = get_number_of_vertex_after_deleting(self.red_A, fix_point_1, fix_point_2)
        self.red_B = get_number_of_vertex_after_deleting(self.red_B, fix_point_1, fix_point_2)


    # pozeram ci nahodou selected 2factor nie je None (None je napriklad vtedy ked nahravam novy file 2faktorov)
    def set_g1_red_and_blue_cycles(self, graph):
        if graph.selected_2factor is None:
            return
        self.g1_involutions_for_current_2factor = graph.find_all_involutions_for_twoFactor(graph.selected_2factor)
        self.combo_box_g1_inv["values"] = self.create_values_for_inv_combo_box(self.g1_involutions_for_current_2factor)
        self.combo_box_g1_inv.current(0)

        involution_2factor = self.g1_involutions_for_current_2factor[0]
        self.g1_blue_cycle = involution_2factor[0]
        self.g1_red_cycle = involution_2factor[1]


    def create_selection_frame(self):
        frame = create_frame(self.g3_main_frame, 2, 0)

        self.v_1 = create_selection_label(frame, "v_1:", "green", 0, 0, 8)
        self.v_2 = create_selection_label(frame, "v_2:", "orange", 1, 0, 8)
        self.z_1 = create_selection_label(frame, "z_1:", "purple", 2, 0, 8)
        self.z_2 = create_selection_label(frame, "z_2:", "gray", 3, 0, 8)

        self.r_A = create_selection_label(frame, "r_A:", "green", 0, 1, 8)
        self.r_B = create_selection_label(frame, "r_B:", "orange", 1, 1, 8)
        self.b_A = create_selection_label(frame, "b_A:", "purple", 2, 1, 8)
        self.b_B = create_selection_label(frame, "b_B:", "gray", 3, 1, 8)

        left_labels = [self.v_1, self.v_2, self.z_1, self.z_2]

        bind_function_to_label(self.v_1, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.v_2, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.z_1, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.z_2, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))

        bind_function_to_label(self.r_A, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.r_B, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.b_A, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.b_B, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))

    def do_correct_connections(self, label1, label2):
        label2.config(background=label1.cget("background"))

        if label1 == self.v_1:

            if label2 == self.r_A:
                color_connect_two_labels(self.z_1, self.b_A)
                color_connect_two_labels(self.v_2, self.r_B)
                color_connect_two_labels(self.z_2, self.b_B)

            elif label2 == self.r_B:
                color_connect_two_labels(self.z_1, self.b_B)
                color_connect_two_labels(self.v_2, self.r_A)
                color_connect_two_labels(self.z_2, self.b_A)

            elif label2 == self.b_A:
                color_connect_two_labels(self.z_1, self.r_A)
                color_connect_two_labels(self.v_2, self.b_B)
                color_connect_two_labels(self.z_2, self.r_B)

            elif label2 == self.b_B:
                color_connect_two_labels(self.z_1, self.r_B)
                color_connect_two_labels(self.v_2, self.b_A)
                color_connect_two_labels(self.z_2, self.r_A)

        elif label1 == self.v_2:

            if label2 == self.r_A:
                color_connect_two_labels(self.z_2, self.b_A)
                color_connect_two_labels(self.v_1, self.r_B)
                color_connect_two_labels(self.z_1, self.b_B)

            elif label2 == self.r_B:
                color_connect_two_labels(self.z_2, self.b_B)
                color_connect_two_labels(self.v_1, self.r_A)
                color_connect_two_labels(self.z_1, self.b_A)

            elif label2 == self.b_A:
                color_connect_two_labels(self.z_2, self.r_A)
                color_connect_two_labels(self.v_1, self.b_B)
                color_connect_two_labels(self.z_1, self.r_B)

            elif label2 == self.b_B:
                color_connect_two_labels(self.z_2, self.r_B)
                color_connect_two_labels(self.v_1, self.b_A)
                color_connect_two_labels(self.z_1, self.r_A)

        elif label1 == self.z_1:

            if label2 == self.r_A:
                color_connect_two_labels(self.v_1, self.b_A)
                color_connect_two_labels(self.z_2, self.r_B)
                color_connect_two_labels(self.v_2, self.b_B)

            elif label2 == self.r_B:
                color_connect_two_labels(self.v_1, self.b_B)
                color_connect_two_labels(self.z_2, self.r_A)
                color_connect_two_labels(self.v_2, self.b_A)

            elif label2 == self.b_A:
                color_connect_two_labels(self.v_1, self.r_A)
                color_connect_two_labels(self.z_2, self.b_B)
                color_connect_two_labels(self.v_2, self.r_B)

            elif label2 == self.b_B:
                color_connect_two_labels(self.v_1, self.r_B)
                color_connect_two_labels(self.z_2, self.b_A)
                color_connect_two_labels(self.v_2, self.r_A)

        elif label1 == self.z_2:

            if label2 == self.r_A:
                color_connect_two_labels(self.v_2, self.b_A)
                color_connect_two_labels(self.z_1, self.r_B)
                color_connect_two_labels(self.v_1, self.b_B)

            elif label2 == self.r_B:
                color_connect_two_labels(self.v_2, self.b_B)
                color_connect_two_labels(self.z_1, self.r_A)
                color_connect_two_labels(self.v_1, self.b_A)

            elif label2 == self.b_A:
                color_connect_two_labels(self.v_2, self.r_A)
                color_connect_two_labels(self.z_1, self.b_B)
                color_connect_two_labels(self.v_1, self.r_B)

            elif label2 == self.b_B:
                color_connect_two_labels(self.v_2, self.r_B)
                color_connect_two_labels(self.z_1, self.b_A)
                color_connect_two_labels(self.v_1, self.r_A)

    # metoda zvyrazni label a nastavi v aplikacii, ze bude vybrata hrana vertex1, vertex2
    # zaroven najde zodpovedajucu hrany zodpovedajuci1 a zodpovedajuci2
    def g1_switch_selected_edge(self, event, vertex1, vertex2, label):
        # tu musim vybrat hranu z nejakeho cyklu, cize nie priecku
        if self.label_is_spoke(label):
            return

        if self.selected_edge_label is not None:
            self.selected_edge_label.config(relief="flat")

        label.config(relief="solid")
        self.selected_edge_label = label

        self.vertex_1 = vertex1
        self.vertex_2 = vertex2
        self.corresponding_1 = find_corresponding_vertex(self.vertex_1, self.g1_blue_cycle, self.g1_red_cycle)
        self.corresponding_2 = find_corresponding_vertex(self.vertex_2, self.g1_blue_cycle, self.g1_red_cycle)

        self.v_1.config(text="v_1:" + str(self.vertex_1))
        self.z_1.config(text="z_1:" + str(self.corresponding_1))
        self.v_2.config(text="v_2:" + str(self.vertex_2))
        self.z_2.config(text="z_2:" + str(self.corresponding_2))

    def get_int_from_labels_by_color(self, labels, color):
        for l in labels:
            if l.cget("background") == color:
                return int(l.cget("text")[4:])

    def function_dipol_construction_1(self):
        if self.check_if_you_can_execute() == False:
            return
        left_labels = [self.v_1, self.v_2, self.z_1, self.z_2]
        green1 = self.get_int_from_labels_by_color(left_labels, "green")
        orange1 = self.get_int_from_labels_by_color(left_labels, "orange")
        purple1 = self.get_int_from_labels_by_color(left_labels, "purple")
        gray1 = self.get_int_from_labels_by_color(left_labels, "gray")

        right_labels = [self.r_A, self.r_B, self.b_A, self.b_B]
        green2 = self.get_int_from_labels_by_color(right_labels, "green")
        orange2 = self.get_int_from_labels_by_color(right_labels, "orange")
        purple2 = self.get_int_from_labels_by_color(right_labels, "purple")
        gray2 = self.get_int_from_labels_by_color(right_labels, "gray")

        fix_point_1 = self.g2_blue_cycle[0]
        fix_point_2 = self.g2_red_cycle[0]

        green2 = get_number_of_vertex_after_deleting(green2, fix_point_1, fix_point_2)
        orange2 = get_number_of_vertex_after_deleting(orange2, fix_point_1, fix_point_2)
        purple2 = get_number_of_vertex_after_deleting(purple2, fix_point_1, fix_point_2)
        gray2 = get_number_of_vertex_after_deleting(gray2, fix_point_1, fix_point_2)

        self.G3 = self.G1.dipol_konstrukcia_1(green1, purple1, orange1, gray1 , self.dipol_adj, green2, orange2, purple2, gray2)
        self.write_g3_to_frame()
        save_to_file_one_graph(self.G3)

    def function_dipol_construction_1_all(self):
        if self.check_if_you_can_execute() == False:
            return
        g1 = self.G1.dipol_konstrukcia_1(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.dipol_adj, self.red_A, self.red_B, self.blue_A, self.blue_B)

        g2 = self.G1.dipol_konstrukcia_1(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.dipol_adj, self.red_B, self.red_A, self.blue_B, self.blue_A)

        g3 = self.G1.dipol_konstrukcia_1(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.dipol_adj, self.blue_A, self.blue_B, self.red_A, self.red_B)

        g4 = self.G1.dipol_konstrukcia_1(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.dipol_adj, self.blue_B, self.blue_A, self.red_B, self.red_A)

        save_to_file([g1, g2, g3, g4])

    def reset_g1_adding_2factor(self):
        # odznacim znvolenu hranu, ak nejaka je
        if self.selected_edge_label is not None:
            self.selected_edge_label.config(relief="flat")

        self.selected_edge_label = None

        # upravim do stavu, ze nebola zvolena hrana
        self.vertex_1 = None
        self.vertex_2 = None
        self.corresponding_1 = None
        self.corresponding_2 = None

        self.v_1.config(text="v_1:")
        self.z_1.config(text="z_1:")
        self.v_2.config(text="v_2:")
        self.z_2.config(text="z_2:")

        self.combo_box_g1_inv["values"] = []
        self.combo_box_g1_inv.set("")
        self.g1_involutions_for_current_2factor = []

        # musim pre G1 znovu nastavit cykly aj vsetko nastavit znovu
        self.set_g1_red_and_blue_cycles(self.G1)

    def reset_g2_adding_2factor(self):
        self.g2_red_cycle = None
        self.g2_blue_cycle = None

        self.r_A.config(text="r_A:")
        self.r_B.config(text="r_B:")
        self.b_A.config(text="b_A:")
        self.b_B.config(text="b_B:")

        self.dipol_adj = None
        self.blue_A = None
        self.blue_B = None

        self.red_A = None
        self.red_B = None

        self.blue_A = None
        self.blue_B = None
        self.red_A = None
        self.red_B = None

        self.combo_box_g2_inv["values"] = []
        self.combo_box_g2_inv.set("")
        self.g2_involutions_for_current_2factor = []

        # znova vytvorim dipol z g2
        self.create_g2_dipol_and_set_cycles(self.G2)

    def handle_setting_cursor_for_labels(self):
        set_cursor_hand_for_labels(self.g1_array_of_labels)

    def change_involution_from_combo_box(self, e, graph):
        index = e.widget.current()

        if graph is self.G1:
            involution = self.g1_involutions_for_current_2factor[index]
            self.g1_red_cycle = involution[0]
            self.g1_blue_cycle = involution[1]

            # spravim funkciu
            # odznacim znvolenu hranu, ak nejaka je
            if self.selected_edge_label is not None:
                self.selected_edge_label.config(relief="flat")

            self.selected_edge_label = None

            # upravim do stavu, ze nebola zvolena hrana
            self.vertex_1 = None
            self.vertex_2 = None
            self.corresponding_1 = None
            self.corresponding_2 = None

            self.v_1.config(text="v_1:")
            self.z_1.config(text="z_1:")
            self.v_2.config(text="v_2:")
            self.z_2.config(text="z_2:")

        elif graph is self.G2:
            involution = self.g2_involutions_for_current_2factor[index]
            self.g2_red_cycle = involution[0]
            self.g2_blue_cycle = involution[1]

            self.r_A.config(text="r_A:")
            self.r_B.config(text="r_B:")
            self.b_A.config(text="b_A:")
            self.b_B.config(text="b_B:")

            self.dipol_adj = None
            self.blue_A = None
            self.blue_B = None

            self.red_A = None
            self.red_B = None

            self.blue_A = None
            self.blue_B = None
            self.red_A = None
            self.red_B = None

            self.create_dipol_from_G2()

    def check_if_you_can_execute(self):
        if self.G1.adjacency_list is None:
            messagebox.showerror('CHYBA', 'Chyba G1')
            return False
        if len(self.G1.twoFactors) == 0:
            messagebox.showerror('CHYBA', 'Chyba G1 2-faktory')
            return False
        if self.G2.adjacency_list is None:
            messagebox.showerror('CHYBA', 'Chyba G2')
            return False
        if len(self.G2.twoFactors) == 0:
            messagebox.showerror('CHYBA', 'Chyba G2 2-faktory')
            return False
        if self.vertex_1 == None:
            messagebox.showerror('CHYBA', 'Zvolte hranu v G1')
            return False
        return True

