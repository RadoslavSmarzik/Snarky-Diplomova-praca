from tkinter import messagebox
from functions import *
from functions_graph import get_neighbous_of_vertex_without_vertex2
from page import Page

# fix1 a fix2 oznacuju vrcholy ktore spojime a medzi, ktore vlozime pevny bod
# unfix1 a unfix2 oznacuje vrcholy ktore iba spojime

# trieda pre konstrukciu 1
class Page_construction_1(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.create_fix_edge_selection()
        self.selected_label = None
        self.vertex1 = None
        self.vertex2 = None

        # fix1 bude vrchol medzi ktory sa bude vkladat pevny bod
        self.fix1 = None
        self.fix2 = None
        self.unfix1 = None
        self.unfix2 = None

        self.g2_main_frame.destroy()

        bind_function_to_button(self.result_button, self.function_construction_1)
        bind_function_to_button(self.result_all_button, self.function_construction_1_all)

    # metoda zvyrazni label a nastavi v aplikacii, ze bola vybrana hrana vertex1 - vertex2 pre G1
    def g1_switch_selected_edge(self, event, vertex1, vertex2, label):
        # vybrana hrana musi byt priecka
        if not self.label_is_spoke(label):
            return

        if self.selected_label is not None:
            self.selected_label.config(relief="flat")
        label.config(relief="solid")
        self.selected_label = label
        self.vertex1 = vertex1
        self.vertex2 = vertex2

        self.set_combo_boxes_fix1_and_fix2()

    def set_combo_boxes_fix1_and_fix2(self):
        vertex1_neighbours = get_neighbous_of_vertex_without_vertex2(self.G1, self.vertex1, self.vertex2)
        vertex2_neighbours = get_neighbous_of_vertex_without_vertex2(self.G1, self.vertex2, self.vertex1)

        self.combo_box_fix_1["values"] = vertex1_neighbours
        self.combo_box_fix_2["values"] = vertex2_neighbours
        self.combo_box_fix_1.current(0)
        self.combo_box_fix_2.current(0)
        self.fix1 = vertex1_neighbours[0]
        self.fix2 = vertex2_neighbours[0]

    def create_fix_edge_selection(self):
        frame = create_frame(self.g3_main_frame, 2, 0)

        self.combo_box_fix_1 = create_combo_box(frame, 0, 0)
        self.combo_box_fix_2 = create_combo_box(frame, 0, 1)

        bind_function_to_combo_box(self.combo_box_fix_1, self.function_combo_box_fix1)
        bind_function_to_combo_box(self.combo_box_fix_2, self.function_combo_box_fix2)

    def function_combo_box_fix1(self, event):
        self.fix1 = int(event.widget.get())

    def function_combo_box_fix2(self, event):
        self.fix2 = int(event.widget.get())

    # funkcia vykona konstrukciu 1
    def function_construction_1(self):
        if self.check_if_you_can_execute() == False:
            return
        self.G3 = self.G1.inv_sym_4_sucin_konstrukcia_1(self.vertex1, self.vertex2, self.fix1, self.fix2)
        self.write_g3_to_frame()
        save_to_file_one_graph(self.G3)

    def function_construction_1_all(self):
        if self.check_if_you_can_execute() == False:
            return
        vertex1_neighbours = get_neighbous_of_vertex_without_vertex2(self.G1, self.vertex1, self.vertex2)
        vertex2_neighbours = get_neighbous_of_vertex_without_vertex2(self.G1, self.vertex2, self.vertex1)

        result_1 = self.G1.inv_sym_4_sucin_konstrukcia_1(self.vertex1, self.vertex2, vertex1_neighbours[0], vertex2_neighbours[0])
        result_2 = self.G1.inv_sym_4_sucin_konstrukcia_1(self.vertex1, self.vertex2, vertex1_neighbours[1], vertex2_neighbours[0])
        result_3 = self.G1.inv_sym_4_sucin_konstrukcia_1(self.vertex1, self.vertex2, vertex1_neighbours[0], vertex2_neighbours[1])
        result_4 = self.G1.inv_sym_4_sucin_konstrukcia_1(self.vertex1, self.vertex2, vertex1_neighbours[1], vertex2_neighbours[1])

        save_to_file([result_1, result_2, result_3, result_4])

    def reset_g1_adding_2factor(self):
        # odznacim label, ak bol zvyrazneny
        if self.selected_label is not None:
            self.selected_label.config(relief="flat")

        # nastavim label na None
        self.selected_label = None

        # vynulujem vertexy
        self.vertex1 = None
        self.vertex2 = None

        # vynulujem fix a unfix vrcholy
        self.fix1 = None
        self.fix2 = None
        self.unfix1 = None
        self.unfix2 = None

        # vynulujem comboboxy pre fix
        self.combo_box_fix_1["values"] = []
        self.combo_box_fix_1.set("")
        self.combo_box_fix_2["values"] = []
        self.combo_box_fix_2.set("")

    def handle_setting_cursor_for_labels(self):
        set_cursor_hand_for_labels(self.g1_array_of_labels)


# funkcia skontroluje, ci je nacitane vsetko potrebne pre vykonanie productu
    def check_if_you_can_execute(self):
        if self.G1.adjacency_list is None:
            messagebox.showerror('CHYBA', 'Chyba G1')
            return False
        if len(self.G1.twoFactors) == 0:
            messagebox.showerror('CHYBA', 'Chyba G1 2-faktory')
            return False

        if self.vertex1 == None or self.vertex2 == None:
            messagebox.showerror('CHYBA', 'Zvolte priečku v G1')
            return False

        return True
