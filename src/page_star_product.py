from functools import partial
from tkinter import messagebox
from functions import *
from page import Page

# trieda pre permutacny 5-sucin
class Page_star_product(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.g1_selected_5cycle = []
        self.g2_selected_5cycle = []

        self.g1_combo_box_5cycles = create_combo_box(self.g1_main_frame, 3, 0)
        self.g2_combo_box_5cycles = create_combo_box(self.g2_main_frame, 3, 0)
        self.g1_combo_box_5cycles.config(width=15)
        self.g2_combo_box_5cycles.config(width=15)

        bind_function_to_button(self.g1_button_add_graph, partial(self.function_loading_graph, self.G1, self.g1_scrollbar_wrapper, self.g1_array_of_labels, self.g1_combo_box_5cycles, self.g1_selected_5cycle))
        bind_function_to_button(self.g2_button_add_graph,partial(self.function_loading_graph, self.G2, self.g2_scrollbar_wrapper,self.g2_array_of_labels, self.g2_combo_box_5cycles, self.g2_selected_5cycle))
        self.create_result_checkboxes()

        bind_function_to_button(self.result_button, self.function_btn_star)
        bind_function_to_button(self.result_all_button, self.function_btn_all_star)

        bind_function_to_combo_box(self.g1_combo_box_5cycles, partial(self.function_combo_5cycles, selected_5cycle=self.g1_selected_5cycle))
        bind_function_to_combo_box(self.g2_combo_box_5cycles, partial(self.function_combo_5cycles, selected_5cycle=self.g2_selected_5cycle))

    def function_loading_graph(self, graph, scrollbar_wrapper, array_of_labels, combo_box, selected_5cycle):
        if self.function_create_graph_from_file(graph, scrollbar_wrapper, array_of_labels) == False:
            return
        self.set_combo_box_5cycles(graph, combo_box, selected_5cycle)

    def set_combo_box_5cycles(self, graph, combo_box, selected_5cycle):
        graph.find_5_cycles(5)
        combo_box["values"] = graph.cycles_of_5
        combo_box.current(0)
        self.set_selected_5cycle(selected_5cycle, graph.cycles_of_5[0])

    def set_selected_5cycle(self, selected_5_cycle, cycle):
        selected_5_cycle.clear()
        for i in range(len(cycle)):
            selected_5_cycle.append(cycle[i])

    def create_result_checkboxes(self):
        frame = create_frame(self.g3_main_frame, row=2, column=0)
        self.g1_checkbox_var = ttk.BooleanVar(value=False)
        self.g2_checkbox_var = ttk.BooleanVar(value=False)
        create_checbox(frame, "G1 opačne", self.g1_checkbox_var)
        create_checbox(frame, "G2 opačne", self.g2_checkbox_var)

    # funkcia vykona 5 sucin
    def function_btn_star(self):
        if self.check_if_you_can_execute() == False:
            return
        self.G3 = self.G1.doStarProduct(self.G2, self.g1_selected_5cycle, self.g2_selected_5cycle, self.G1.selected_2factor,self.G2.selected_2factor, self.g1_checkbox_var.get(), self.g2_checkbox_var.get())
        self.write_g3_to_frame()
        save_to_file_one_graph(self.G3)

    # funkcia vykona vsetky mozne 5suciny
    def function_btn_all_star(self):
        if self.check_if_you_can_execute() == False:
            return
        star_1 = self.G1.doStarProduct(self.G2, self.g1_selected_5cycle, self.g2_selected_5cycle, self.G1.selected_2factor,
                                       self.G2.selected_2factor, False, False)
        star_2 = self.G1.doStarProduct(self.G2, self.g1_selected_5cycle, self.g2_selected_5cycle, self.G1.selected_2factor,
                                       self.G2.selected_2factor, False, True)
        star_3 = self.G1.doStarProduct(self.G2, self.g1_selected_5cycle, self.g2_selected_5cycle, self.G1.selected_2factor,
                                       self.G2.selected_2factor, True, False)
        star_4 = self.G1.doStarProduct(self.G2, self.g1_selected_5cycle, self.g2_selected_5cycle, self.G1.selected_2factor,
                                       self.G2.selected_2factor, True, True)
        save_to_file([star_1, star_2, star_3, star_4])

    def function_combo_5cycles(self, event, selected_5cycle):
        self.set_selected_5cycle(selected_5cycle, [int(i) for i in event.widget.get().split(" ")])

    def reset_g1_adding(self):
        self.g1_selected_5cycle.clear()
        self.g1_combo_box_5cycles["values"] = []
        self.g1_combo_box_5cycles.set("")
        Page.reset_g1_adding(self)


    def reset_g2_adding(self):
        self.g2_selected_5cycle.clear()
        self.g2_combo_box_5cycles["values"] = []
        self.g2_combo_box_5cycles.set("")
        Page.reset_g2_adding(self)

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




