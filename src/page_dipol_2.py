from functools import partial
from tkinter import messagebox
from functions import *
from functions_graph import *
from page import Page

# trieda pre vkladanie permutacnych dipolov
class Page_dipol_2(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_selection_frame()
        bind_function_to_button(self.g1_button_add_2factors, partial(self.function_load_2factor_g1, self.G1, self.g1_combo_box, self.g1_array_of_labels))

        self.selected_selection_lbl = None
        bind_function_to_button(self.result_button, self.function_dipol_construction_2)
        bind_function_to_button(self.result_all_button, self.function_dipol_construction_2_all)

        self.g1_e1_selected_lbl = None
        self.g1_e2_selected_lbl = None

        self.g2_spoke = None
        self.fix_point_1 = None
        self.fix_point_2 = None

        self.create_inv_combo_boxes()
        self.g1_involutions_for_current_2factor = []
        self.combo_box_g2_inv.destroy()

        self.vertex_1 = None
        self.vertex_2 = None
        self.vertex_3 = None
        self.vertex_4 = None
        self.corresponding_1 = None  # zodpovedajuci
        self.corresponding_2 = None
        self.corresponding_3 = None
        self.corresponding_4 = None

    def function_load_2factor_g1(self, graph, combo_box, array_of_labels):
        self.function_load_2factors_from_file(graph, combo_box, array_of_labels, filter_involution_2_factors=True)
        self.set_g1_red_and_blue_cycles(graph)

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
        self.z_3 = create_selection_label(frame, "z_3:", "purple", 2, 0, 8)
        self.z_4 = create_selection_label(frame, "z_4:", "gray", 3, 0, 8)

        self.r_A = create_selection_label(frame, "r_A:", "green", 0, 1, 8)
        self.r_B = create_selection_label(frame, "r_B:", "orange", 1, 1, 8)
        self.b_A = create_selection_label(frame, "b_A:", "purple", 2, 1, 8)
        self.b_B = create_selection_label(frame, "b_B:", "gray", 3, 1, 8)

        left_labels = [self.v_1, self.v_2, self.z_3, self.z_4]

        bind_function_to_label(self.v_1, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.v_2, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.z_3, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.z_4, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))

        bind_function_to_label(self.r_A, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.r_B, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.b_A, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.b_B, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))

    def do_correct_connections(self, label1, label2):
        label2.config(background=label1.cget("background"))

        if label1 == self.v_1:

            if label2 == self.r_A:
                color_connect_two_labels(self.v_2, self.r_B)
                self.do_correct_reconnection(self.z_3, self.z_4, self.b_A, self.b_B)

            elif label2 == self.r_B:
                color_connect_two_labels(self.v_2, self.r_A)
                self.do_correct_reconnection(self.z_3, self.z_4, self.b_A, self.b_B)

            elif label2 == self.b_A:
                color_connect_two_labels(self.v_2, self.b_B)
                self.do_correct_reconnection(self.z_3, self.z_4, self.r_A, self.r_B)

            elif label2 == self.b_B:
                color_connect_two_labels(self.v_2, self.b_A)
                self.do_correct_reconnection(self.z_3, self.z_4, self.r_A, self.r_B)

        elif label1 == self.v_2:

            if label2 == self.r_A:
                color_connect_two_labels(self.v_1, self.r_B)
                self.do_correct_reconnection(self.z_3, self.z_4, self.b_A, self.b_B)

            elif label2 == self.r_B:
                color_connect_two_labels(self.v_1, self.r_A)
                self.do_correct_reconnection(self.z_3, self.z_4, self.b_A, self.b_B)

            elif label2 == self.b_A:
                color_connect_two_labels(self.v_1, self.b_B)
                self.do_correct_reconnection(self.z_3, self.z_4, self.r_A, self.r_B)

            elif label2 == self.b_B:
                color_connect_two_labels(self.v_1, self.b_A)
                self.do_correct_reconnection(self.z_3, self.z_4, self.r_A, self.r_B)

        elif label1 == self.z_3:

            if label2 == self.r_A:
                color_connect_two_labels(self.z_4, self.r_B)
                self.do_correct_reconnection(self.v_1, self.v_2, self.b_A, self.b_B)

            elif label2 == self.r_B:
                color_connect_two_labels(self.z_4, self.r_A)
                self.do_correct_reconnection(self.v_1, self.v_2, self.b_A, self.b_B)

            elif label2 == self.b_A:
                color_connect_two_labels(self.z_4, self.b_B)
                self.do_correct_reconnection(self.v_1, self.v_2, self.r_A, self.r_B)

            elif label2 == self.b_B:
                color_connect_two_labels(self.z_4, self.b_A)
                self.do_correct_reconnection(self.v_1, self.v_2, self.r_A, self.r_B)

        elif label1 == self.z_4:

            if label2 == self.r_A:
                color_connect_two_labels(self.z_3, self.r_B)
                self.do_correct_reconnection(self.v_1, self.v_2, self.b_A, self.b_B)

            elif label2 == self.r_B:
                color_connect_two_labels(self.z_3, self.r_A)
                self.do_correct_reconnection(self.v_1, self.v_2, self.b_A, self.b_B)

            elif label2 == self.b_A:
                color_connect_two_labels(self.z_3, self.b_B)
                self.do_correct_reconnection(self.v_1, self.v_2, self.r_A, self.r_B)

            elif label2 == self.b_B:
                color_connect_two_labels(self.z_3, self.b_A)
                self.do_correct_reconnection(self.v_1, self.v_2, self.r_A, self.r_B)

    # metoda zvyrazni label a nastavi v aplikacii, ze bude vybrata hrana vertex1, vertex2
    # zaroven najde zodpovedajucu hrany zodpovedajuci1 a zodpovedajuci2
    # zatial mozem vyberat iba hrany rovnakej farby (mozno zmenim)
    def g1_switch_selected_edge(self, event, vertex1, vertex2, label):
        # ak som klikol na priecku, hned koniec
        if self.label_is_spoke(label):
            return

        # ak label bol zvyrazneny ako hrana e1, tak ho odznac a vynuluj
        if label is self.g1_e1_selected_lbl:
            label.config(relief="flat")
            self.vertex_1 = None
            self.vertex_2 = None
            self.corresponding_1 = None
            self.corresponding_2 =None

            self.v_1.config(text="v_1:")
            self.v_2.config(text="v_2:")

            self.g1_e1_selected_lbl = None
            return

        # ak label bol zvyrazneny ako hrana e2, tak ho odznac a vynuluj
        if label is self.g1_e2_selected_lbl:
            label.config(relief="flat")
            self.vertex_3 = None
            self.vertex_4 = None
            self.corresponding_3 = None
            self.corresponding_4 = None

            self.z_3.config(text="z_3:")
            self.z_4.config(text="z_4:")

            self.g1_e2_selected_lbl = None
            return

        # ak je hrana e1 prazdna, tak ju nastav na hranu vertex1 - vertex2
        # ak nie je tak prepis hranu e2, nech bola alebo nebola oznacena
        if self.g1_e1_selected_lbl is None:

            # pozriem sa ci e2 ma rovnaku farbu ako label
            if self.g1_e2_selected_lbl is not None:
                if not self.labels_have_same_color(label, self.g1_e2_selected_lbl):
                    return

            self.vertex_1 = vertex1
            self.vertex_2 = vertex2
            self.corresponding_1 = find_corresponding_vertex(self.vertex_1, self.g1_blue_cycle, self.g1_red_cycle)
            self.corresponding_2 = find_corresponding_vertex(self.vertex_2, self.g1_blue_cycle, self.g1_red_cycle)
            self.g1_e1_selected_lbl = label

            self.v_1.config(text="v_1:" + str(self.vertex_1))
            self.v_2.config(text="v_2:" + str(self.vertex_2))

        else:
            # pozriem sa ci e1 ma rovnaku farbu ako label
            if self.g1_e1_selected_lbl is not None:
                if not self.labels_have_same_color(label, self.g1_e1_selected_lbl):
                    return

            if self.g1_e2_selected_lbl is not None:
                    self.g1_e2_selected_lbl.config(relief="flat")
            self.vertex_3 = vertex1
            self.vertex_4 = vertex2
            self.corresponding_3 = find_corresponding_vertex(self.vertex_3, self.g1_blue_cycle, self.g1_red_cycle)
            self.corresponding_4 = find_corresponding_vertex(self.vertex_4, self.g1_blue_cycle, self.g1_red_cycle)
            self.g1_e2_selected_lbl = label

            self.z_3.config(text="z_3:" + str(self.corresponding_3))
            self.z_4.config(text="z_4:" + str(self.corresponding_4))

        # zvyrazni label
        label.config(relief="solid")

    def get_int_from_labels_by_color(self, labels, color):
        for l in labels:
            if l.cget("background") == color:
                return int(l.cget("text")[4:])

    def function_dipol_construction_2(self):
        if self.check_if_you_can_execute() == False:
            return
        right_labels = [self.r_A, self.r_B, self.b_A, self.b_B]
        green2 = self.get_int_from_labels_by_color(right_labels, "green")
        orange2 = self.get_int_from_labels_by_color(right_labels, "orange")
        purple2 = self.get_int_from_labels_by_color(right_labels, "purple")
        gray2 = self.get_int_from_labels_by_color(right_labels, "gray")

        green2 = get_number_of_vertex_after_deleting(green2, self.fix_point_1, self.fix_point_2)
        orange2 = get_number_of_vertex_after_deleting(orange2, self.fix_point_1, self.fix_point_2)
        purple2 = get_number_of_vertex_after_deleting(purple2, self.fix_point_1, self.fix_point_2)
        gray2 = get_number_of_vertex_after_deleting(gray2, self.fix_point_1, self.fix_point_2)

        self.G3 = self.G1.dipol_konstrukcia_2(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                              self.vertex_3, self.corresponding_3, self.vertex_4, self.corresponding_4,
                                              self.G2, green2, orange2, purple2, gray2, self.fix_point_1, self.fix_point_2)

        self.write_g3_to_frame()
        save_to_file_one_graph(self.G3)


    def function_dipol_construction_2_all(self):
        if self.check_if_you_can_execute() == False:
            return
        red_A = int(self.r_A.cget("text")[4:])
        red_B = int(self.r_B.cget("text")[4:])
        blue_A = int(self.b_A.cget("text")[4:])
        blue_B = int(self.b_B.cget("text")[4:])

        red_A = get_number_of_vertex_after_deleting(red_A, self.fix_point_1, self.fix_point_2)
        red_B = get_number_of_vertex_after_deleting(red_B, self.fix_point_1, self.fix_point_2)
        blue_A = get_number_of_vertex_after_deleting(blue_A, self.fix_point_1, self.fix_point_2)
        blue_B = get_number_of_vertex_after_deleting(blue_B, self.fix_point_1, self.fix_point_2)

        g1 = self.G1.dipol_konstrukcia_2(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.vertex_3, self.corresponding_3, self.vertex_4, self.corresponding_4,
                                         self.G2, red_A, red_B, blue_A, blue_B,
                                         self.fix_point_1, self.fix_point_2)

        g2 = self.G1.dipol_konstrukcia_2(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.vertex_3, self.corresponding_3, self.vertex_4, self.corresponding_4,
                                         self.G2, red_B, red_A, blue_B, blue_A,
                                         self.fix_point_1, self.fix_point_2)

        g3 = self.G1.dipol_konstrukcia_2(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.vertex_3, self.corresponding_3, self.vertex_4, self.corresponding_4,
                                         self.G2, blue_A, blue_B, red_A, red_B,
                                         self.fix_point_1, self.fix_point_2)

        g4 = self.G1.dipol_konstrukcia_2(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.vertex_3, self.corresponding_3, self.vertex_4, self.corresponding_4,
                                         self.G2, blue_B, blue_A, red_B, red_A,
                                         self.fix_point_1, self.fix_point_2)

        g5 = self.G1.dipol_konstrukcia_2(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.vertex_3, self.corresponding_3, self.vertex_4, self.corresponding_4,
                                         self.G2, red_A, red_B, blue_B, blue_A,
                                         self.fix_point_1, self.fix_point_2)

        g6 = self.G1.dipol_konstrukcia_2(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.vertex_3, self.corresponding_3, self.vertex_4, self.corresponding_4,
                                         self.G2, red_B, red_A, blue_A, blue_B,
                                         self.fix_point_1, self.fix_point_2)

        g7 = self.G1.dipol_konstrukcia_2(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.vertex_3, self.corresponding_3, self.vertex_4, self.corresponding_4,
                                         self.G2, blue_A, blue_B, red_B, red_A,
                                         self.fix_point_1, self.fix_point_2)

        g8 = self.G1.dipol_konstrukcia_2(self.vertex_1, self.corresponding_1, self.vertex_2, self.corresponding_2,
                                         self.vertex_3, self.corresponding_3, self.vertex_4, self.corresponding_4,
                                         self.G2, blue_B, blue_A, red_A, red_B,
                                         self.fix_point_1, self.fix_point_2)

        save_to_file([g1, g2, g3, g4, g5, g6, g7, g8])


    # farba z lavych labelov musi byt aj v tych v pravo
    def do_correct_reconnection(self, label_left_1, label_left_2, label_right_1, label_right_2):
        color1 = label_left_1.cget("background")
        color2 = label_left_2.cget("background")
        color3 = label_right_1.cget("background")
        color4 = label_right_2.cget("background")

        if color1 == color3 or color1 == color4:
            if color2 == color3 or color2 == color4:
                return
        color_connect_two_labels(label_left_1, label_right_1)
        color_connect_two_labels(label_left_2, label_right_2)

    # metoda pre preoznacenie priecky v grafe G2
    def g2_switch_selected_edge(self, event, vertex1, vertex2, label):
        # ak nahodou nie je priecka, tak hned koniec
        if not self.label_is_spoke(label):
            return

        # ak bol nejaky selected label tak ho odznacim
        if self.g2_spoke is not None:
            self.g2_spoke.config(relief="flat")

        # ak som klikol na taky, co uz predtym bol tak ho odznacim a skoncim
        if self.g2_spoke is label:
            self.g2_spoke = None
            self.r_A.config(text="r_A:")
            self.r_B.config(text="r_B:")
            self.b_A.config(text="b_A:")
            self.b_B.config(text="b_B:")
            self.fix_point_1 = None
            self.fix_point_2 = None
            return

        # inac zvyraznim ten na ktory som klikol
        self.g2_spoke = label
        red_verticies = get_neighbous_of_vertex_without_vertex2(self.G2, vertex1, vertex2)
        blue_verticies = get_neighbous_of_vertex_without_vertex2(self.G2, vertex2, vertex1)
        self.r_A.config(text="r_A:" + str(red_verticies[0]))
        self.r_B.config(text="r_B:" + str(red_verticies[1]))
        self.b_A.config(text="b_A:" + str(blue_verticies[0]))
        self.b_B.config(text="b_B:" + str(blue_verticies[1]))
        self.fix_point_1 = vertex1
        self.fix_point_2 = vertex2
        label.config(relief="solid")

    def reset_g1_adding_2factor(self):
        # vyzualne odznacim labely
        if self.g1_e1_selected_lbl is not None:
            self.g1_e1_selected_lbl.config(relief="flat")
        if self.g1_e2_selected_lbl is not None:
            self.g1_e2_selected_lbl.config(relief="flat")

        # odznacim labely logicky
        self.g1_e1_selected_lbl = None
        self.g1_e2_selected_lbl = None

        # upravim selectovanie
        self.v_1.config(text="v_1:")
        self.v_2.config(text="v_2:")
        self.z_3.config(text="z_3:")
        self.z_4.config(text="z_4:")

        # vsetky vertexy a zodpovedajuce k nim dam na None
        self.vertex_1 = None
        self.vertex_2 = None
        self.vertex_3 = None
        self.vertex_4 = None
        self.corresponding_1 = None
        self.corresponding_2 = None
        self.corresponding_3 = None
        self.corresponding_4 = None


        self.g1_involutions_for_current_2factor = []

        # podla nastaveneho 2faktora nastavim cykly pre G1
        self.set_g1_red_and_blue_cycles(self.G1)


    def reset_g2_adding_2factor(self):
        if self.g2_spoke is not None:
            self.g2_spoke.config(relief="flat")

        self.g2_spoke = None

        self.r_A.config(text="r_A:")
        self.r_B.config(text="r_B:")
        self.b_A.config(text="b_A:")
        self.b_B.config(text="b_B:")
        self.fix_point_1 = None
        self.fix_point_2 = None

    def handle_setting_cursor_for_labels(self):
        set_cursor_hand_for_labels(self.g1_array_of_labels)
        set_cursor_hand_for_labels(self.g2_array_of_labels)

    def change_involution_from_combo_box(self, e, graph):
        index = e.widget.current()

        if graph is self.G1:
            involution_2factor = self.g1_involutions_for_current_2factor[index]
            self.g1_blue_cycle = involution_2factor[0]
            self.g1_red_cycle = involution_2factor[1]

            # vyzualne odznacim labely
            if self.g1_e1_selected_lbl is not None:
                self.g1_e1_selected_lbl.config(relief="flat")
            if self.g1_e2_selected_lbl is not None:
                self.g1_e2_selected_lbl.config(relief="flat")

            # odznacim labely logicky
            self.g1_e1_selected_lbl = None
            self.g1_e2_selected_lbl = None

            # upravim selectovanie
            self.v_1.config(text="v_1:")
            self.v_2.config(text="v_2:")
            self.z_3.config(text="z_3:")
            self.z_4.config(text="z_4:")

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

        if self.vertex_3 == None:
            messagebox.showerror('CHYBA', 'Zvolte hranu v G1')
            return False

        if self.fix_point_1  == None:
            messagebox.showerror('CHYBA', 'Zvolte priečku v G2')
            return False

        return True



