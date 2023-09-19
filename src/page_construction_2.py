from functools import partial
from tkinter import messagebox
from functions import *
from page import Page

# trieda pre konstrukciu 2
class Page_construction_2(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_selection_choice_frame()

        self.selected_selection_lbl = None

        self.create_inv_combo_boxes()

        bind_function_to_button(self.g1_button_add_2factors, partial(self.function_load_2factor, self.G1, self.g1_combo_box, self.g1_array_of_labels))
        bind_function_to_button(self.g2_button_add_2factors, partial(self.function_load_2factor, self.G2, self.g2_combo_box, self.g2_array_of_labels))

        bind_function_to_button(self.result_button, self.function_construction_2)
        bind_function_to_button(self.result_all_button, self.function_construction_2_all)

        self.g1_involutions_for_current_2factor = []
        self.g2_involution_for_current_2factor = []

    def function_load_2factor(self, graph, combo_box, array_of_labels):
        self.function_load_2factors_from_file(graph, combo_box, array_of_labels, filter_involution_2_factors=True)
        self.set_selections_labels_after_load_or_change(graph)

    def set_selections_labels_after_load_or_change(self, graph):
        if graph.selected_2factor is None:
            return

        # najdem vsetky involucie pre zvoleny 2faktor
        all_involutions_for_2factor = graph.find_all_involutions_for_twoFactor(graph.selected_2factor)

        involution_2factor = all_involutions_for_2factor[0]
        red_1 = involution_2factor[0][1]
        blue_1 = involution_2factor[1][1]
        red_last = involution_2factor[0][-1]
        blue_last = involution_2factor[1][-1]
        
        if graph is self.G1:
            self.g1_involutions_for_current_2factor = all_involutions_for_2factor
            self.combo_box_g1_inv["values"] = self.create_values_for_inv_combo_box(all_involutions_for_2factor)
            self.combo_box_g1_inv.current(0)

            self.g1_fix_point = [involution_2factor[0][0], involution_2factor[1][0]]
            self.c_A.config(text="c_A:" + str(red_1))
            self.c_B.config(text="c_B:" + str(red_last))
            self.m_A.config(text="m_A:" + str(blue_1))
            self.m_B.config(text="m_B:" + str(blue_last))

        elif graph is self.G2:
            self.g2_involutions_for_2factor = all_involutions_for_2factor
            self.combo_box_g2_inv["values"] = self.create_values_for_inv_combo_box(all_involutions_for_2factor)
            self.combo_box_g2_inv.current(0)

            self.g2_fix_point = [involution_2factor[0][0], involution_2factor[1][0]]
            self.c_C.config(text="c_C:" + str(red_1))
            self.c_D.config(text="c_D:" + str(red_last))
            self.m_C.config(text="m_C:" + str(blue_1))
            self.m_D.config(text="m_d:" + str(blue_last))

    def change_involution_from_combo_box(self,e, graph):
        index = e.widget.current()

        if graph is self.G1:
            involution = self.g1_involutions_for_current_2factor[index]
        elif graph is self.G2:
            involution = self.g2_involutions_for_2factor[index]

        red_1 = involution[0][1]
        blue_1 = involution[1][1]
        red_last = involution[0][-1]
        blue_last = involution[1][-1]

        if graph is self.G1:
            self.g1_fix_point = [involution[0][0], involution[1][0]]
            self.c_A.config(text="c_A:" + str(red_1))
            self.c_B.config(text="c_B:" + str(red_last))
            self.m_A.config(text="m_A:" + str(blue_1))
            self.m_B.config(text="m_B:" + str(blue_last))

        elif graph is self.G2:
            self.g2_fix_point = [involution[0][0], involution[1][0]]
            self.c_C.config(text="c_C:" + str(red_1))
            self.c_D.config(text="c_D:" + str(red_last))
            self.m_C.config(text="m_C:" + str(blue_1))
            self.m_D.config(text="m_d:" + str(blue_last))

    def create_selection_choice_frame(self):
        frame = create_frame(self.g3_main_frame, 2, 0)

        self.radiobutton_variable = StringVar(frame, "green")

        create_radiobutton(frame, self.radiobutton_variable, "green", 0, 0)
        create_radiobutton(frame, self.radiobutton_variable, "orange", 1, 0)
        create_radiobutton(frame, self.radiobutton_variable, "purple", 2, 0)
        create_radiobutton(frame, self.radiobutton_variable, "gray", 3, 0)

        self.c_A = create_selection_label(frame, "c_A:", "green", 0, 1, 8)
        self.c_B = create_selection_label(frame, "c_B:", "orange", 1, 1, 8)
        self.m_A = create_selection_label(frame, "m_A:", "purple", 2, 1, 8)
        self.m_B = create_selection_label(frame, "m_B:", "gray", 3, 1, 8)

        self.c_C = create_selection_label(frame, "c_C:", "green", 0, 2, 8)
        self.c_D = create_selection_label(frame, "c_D:", "orange", 1, 2, 8)
        self.m_C = create_selection_label(frame, "m_C:", "purple", 2, 2, 8)
        self.m_D = create_selection_label(frame, "m_D:", "gray", 3, 2, 8)

        left_labels = [self.c_A, self.c_B, self.m_A, self.m_B]

        bind_function_to_label(self.c_A, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.c_B, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.m_A, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.m_B, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))

        bind_function_to_label(self.c_C, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.c_D, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.m_C, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))
        bind_function_to_label(self.m_D, partial(self.handle_click_on_selection_label, left_side_labels=left_labels))

    def do_correct_connections(self, label1, label2):
        label2.config(background=label1.cget("background"))

        if label1 == self.c_A:

            if label2 == self.c_C:
                color_connect_two_labels(self.m_A, self.m_C)
                color_connect_two_labels(self.c_B, self.c_D)
                color_connect_two_labels(self.m_B, self.m_D)

            elif label2 == self.c_D:
                color_connect_two_labels(self.m_A, self.m_D)
                color_connect_two_labels(self.c_B, self.c_C)
                color_connect_two_labels(self.m_B, self.m_C)

            elif label2 == self.m_C:
                color_connect_two_labels(self.m_A, self.c_C)
                color_connect_two_labels(self.c_B, self.m_D)
                color_connect_two_labels(self.m_B, self.c_D)

            elif label2 == self.m_D:
                color_connect_two_labels(self.m_A, self.c_D)
                color_connect_two_labels(self.c_B, self.m_C)
                color_connect_two_labels(self.m_B, self.c_C)

        elif label1 == self.c_B:

            if label2 == self.c_C:
                color_connect_two_labels(self.m_B, self.m_C)
                color_connect_two_labels(self.c_A, self.c_D)
                color_connect_two_labels(self.m_A, self.m_D)

            elif label2 == self.c_D:
                color_connect_two_labels(self.m_B, self.m_D)
                color_connect_two_labels(self.c_A, self.c_C)
                color_connect_two_labels(self.m_A, self.m_C)

            elif label2 == self.m_C:
                color_connect_two_labels(self.m_B, self.c_C)
                color_connect_two_labels(self.c_A, self.m_D)
                color_connect_two_labels(self.m_A, self.c_D)

            elif label2 == self.m_D:
                color_connect_two_labels(self.m_B, self.c_D)
                color_connect_two_labels(self.c_A, self.m_C)
                color_connect_two_labels(self.m_A, self.c_C)

        elif label1 == self.m_A:

            if label2 == self.c_C:
                color_connect_two_labels(self.c_A, self.m_C)
                color_connect_two_labels(self.c_B, self.m_D)
                color_connect_two_labels(self.m_B, self.c_D)

            elif label2 == self.c_D:
                color_connect_two_labels(self.c_A, self.m_D)
                color_connect_two_labels(self.c_B, self.m_C)
                color_connect_two_labels(self.m_B, self.c_C)

            elif label2 == self.m_C:
                color_connect_two_labels(self.c_A, self.c_C)
                color_connect_two_labels(self.c_B, self.c_D)
                color_connect_two_labels(self.m_B, self.m_D)

            elif label2 == self.m_D:
                color_connect_two_labels(self.c_A, self.c_D)
                color_connect_two_labels(self.c_B, self.c_C)
                color_connect_two_labels(self.m_B, self.m_C)

        elif label1 == self.m_B:

            if label2 == self.c_C:
                color_connect_two_labels(self.c_B, self.m_C)
                color_connect_two_labels(self.c_A, self.m_D)
                color_connect_two_labels(self.m_A, self.c_D)

            elif label2 == self.c_D:
                color_connect_two_labels(self.c_B, self.m_D)
                color_connect_two_labels(self.c_A, self.m_C)
                color_connect_two_labels(self.m_A, self.c_C)

            elif label2 == self.m_C:
                color_connect_two_labels(self.c_B, self.c_C)
                color_connect_two_labels(self.c_A, self.c_D)
                color_connect_two_labels(self.m_A, self.m_D)

            elif label2 == self.m_D:
                color_connect_two_labels(self.c_B, self.c_D)
                color_connect_two_labels(self.c_A, self.c_C)
                color_connect_two_labels(self.m_A, self.m_C)

    def function_construction_2(self):
        if self.check_if_you_can_execute() == False:
            return
        array_of_labels = [self.c_A, self.c_B, self.m_A, self.m_B]
        green1 = self.get_int_from_labels_by_color(array_of_labels, "green")
        orange1 = self.get_int_from_labels_by_color(array_of_labels, "orange")
        purple1 = self.get_int_from_labels_by_color(array_of_labels, "purple")
        gray1 = self.get_int_from_labels_by_color(array_of_labels, "gray")

        array_of_labels = [self.c_C, self.c_D, self.m_C, self.m_D]
        green2 = self.get_int_from_labels_by_color(array_of_labels, "green")
        orange2 = self.get_int_from_labels_by_color(array_of_labels, "orange")
        purple2 = self.get_int_from_labels_by_color(array_of_labels, "purple")
        gray2 = self.get_int_from_labels_by_color(array_of_labels, "gray")

        choosen_color = self.radiobutton_variable.get()

        # g2_fix_1 - znamena ze vrchol je z g2 a bude tvorit hranu fix_1 pricom medzi hranu fix_1 bude vlozeny pevny bod
        if choosen_color == "green" or choosen_color == "purple":
            g1_fix_1 = green1
            g2_fix_1 = green2
            g1_fix_2 = purple1
            g2_fix_2 = purple2

            g1_unfix_1 = orange1
            g2_unfix_1 = orange2
            g1_unfix_2 = gray1
            g2_unfix_2 = gray2

        elif choosen_color == "orange" or choosen_color == "gray":
            g1_fix_1 = orange1
            g2_fix_1 = orange2
            g1_fix_2 = gray1
            g2_fix_2 = gray2

            g1_unfix_1 = green1
            g2_unfix_1 = green2
            g1_unfix_2 = purple1
            g2_unfix_2 = purple2

        self.G3 = self.G1.inv_sym_4_konstrukcia_2(self.G2, g1_fix_1, g2_fix_1, g1_fix_2, g2_fix_2, g1_unfix_1, g2_unfix_1, g1_unfix_2, g2_unfix_2, self.g1_fix_point[0], self.g1_fix_point[1], self.g2_fix_point[0], self.g2_fix_point[1], )
        self.write_g3_to_frame()
        save_to_file_one_graph(self.G3)

    def get_int_from_labels_by_color(self, labels, color):
        for l in labels:
            if l.cget("background") == color:
                return int(l.cget("text")[4:])

    def function_construction_2_all(self):
        if self.check_if_you_can_execute() == False:
            return
        c_A = int(self.c_A.cget("text")[4:])
        c_B = int(self.c_B.cget("text")[4:])
        m_A = int(self.m_A.cget("text")[4:])
        m_B = int(self.m_B.cget("text")[4:])

        c_C = int(self.c_C.cget("text")[4:])
        c_D = int(self.c_D.cget("text")[4:])
        m_C = int(self.m_C.cget("text")[4:])
        m_D = int(self.m_D.cget("text")[4:])

        # hranova = c_A + c_C
        kon2_1 = self.G1.inv_sym_4_konstrukcia_2(self.G2, c_A, c_C, m_A, m_C,
                                                c_B, c_D, m_B, m_D,
                                                self.g1_fix_point[0], self.g1_fix_point[1],
                                                self.g2_fix_point[0], self.g2_fix_point[1])

        # hranova = c_A + c_D (ROVNAKO aj hranova = m_A + m_D)
        kon2_2 = self.G1.inv_sym_4_konstrukcia_2(self.G2, c_A, c_D, m_A, m_D,
                                                 c_B, c_C, m_B, m_C,
                                                 self.g1_fix_point[0], self.g1_fix_point[1],
                                                 self.g2_fix_point[0], self.g2_fix_point[1])

        # hranova = c_A + m_C
        kon2_3 = self.G1.inv_sym_4_konstrukcia_2(self.G2, c_A, m_C, m_A, c_C,
                                                 c_B, m_D, m_B, c_D,
                                                 self.g1_fix_point[0], self.g1_fix_point[1],
                                                 self.g2_fix_point[0], self.g2_fix_point[1])

        # hranova = c_A + m_D
        kon2_4 = self.G1.inv_sym_4_konstrukcia_2(self.G2, c_A, m_D, m_A, c_D,
                                                 c_B, m_C, m_B, c_C,
                                                 self.g1_fix_point[0], self.g1_fix_point[1],
                                                 self.g2_fix_point[0], self.g2_fix_point[1])

        # hranova = c_B + c_C
        kon2_5 = self.G1.inv_sym_4_konstrukcia_2(self.G2, c_B, c_C, m_B, m_C,
                                                 c_A, c_D, m_A, m_D,
                                                 self.g1_fix_point[0], self.g1_fix_point[1],
                                                 self.g2_fix_point[0], self.g2_fix_point[1])

        # hranova = c_B + c_D
        kon2_6 = self.G1.inv_sym_4_konstrukcia_2(self.G2, c_B, c_D, m_B, m_D,
                                                 c_A, c_C, m_A, m_C,
                                                 self.g1_fix_point[0], self.g1_fix_point[1],
                                                 self.g2_fix_point[0], self.g2_fix_point[1])

        # hranova = c_B + m_C
        kon2_7 = self.G1.inv_sym_4_konstrukcia_2(self.G2, c_B, m_C, m_B, c_C,
                                                 c_A, m_D, m_A, c_D,
                                                 self.g1_fix_point[0], self.g1_fix_point[1],
                                                 self.g2_fix_point[0], self.g2_fix_point[1])

        # hranova = c_B + m_D
        kon2_8 = self.G1.inv_sym_4_konstrukcia_2(self.G2, c_B, m_D, m_B, c_D,
                                                 c_A, m_C, m_A, c_C,
                                                 self.g1_fix_point[0], self.g1_fix_point[1],
                                                 self.g2_fix_point[0], self.g2_fix_point[1])

        array_of_graphs = [kon2_1, kon2_2, kon2_3, kon2_4, kon2_5, kon2_6, kon2_7, kon2_8]
        save_to_file(array_of_graphs)

    def reset_g1_adding_2factor(self):
        # v self.G1.selected_2factor mam ulozeny vybrany 2faktor
        # z tohto selected 2faktora skusim najst involuciu a spravim znovu tu istu vec ako pri nacitani

        self.c_A.config(text="c_A:")
        self.c_B.config(text="c_B:")
        self.m_A.config(text="m_A:")
        self.m_B.config(text="m_B:")

        self.combo_box_g1_inv["values"] = []
        self.combo_box_g1_inv.set("")

        self.g1_involutions_for_current_2factor = []

        self.set_selections_labels_after_load_or_change(self.G1)

    def reset_g2_adding_2factor(self):
        self.c_C.config(text="c_C:")
        self.c_D.config(text="c_D:")
        self.m_C.config(text="m_C:")
        self.m_D.config(text="m_d:")

        self.combo_box_g2_inv["values"] = []
        self.combo_box_g2_inv.set("")

        self.g2_involution_for_current_2factor = []

        self.set_selections_labels_after_load_or_change(self.G2)

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
        return True

