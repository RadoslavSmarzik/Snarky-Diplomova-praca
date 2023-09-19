from functools import partial
from tkinter import messagebox
from functions import *
from graph import Graph, TwoFactor

# G1 - graf 1 matematicky
# G2 - graf 2 matematicky
# g1_array_of_labels - pole v ktorom su ulozene labely, na ktore sa da klikat a ktore reprezentuju hrany (vrcholy)
# g1_button_add_graph -
# g1_main_frame - hlavne okno pre G1

# nadtrieda pre vsetky page classy
class Page(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.G1 = Graph()
        self.g1_array_of_labels = []
        self.create_g1_widgets()

        self.G2 = Graph()
        self.g2_array_of_labels = []
        self.create_g2_widgets()

        self.G3 = Graph()
        self.create_g3_widgets()

    def show(self):
        self.lift()

    # funkcia vytvori zakladne widgety pre graf G1
    def create_g1_widgets(self):
        self.g1_main_frame = create_frame(self, 0, 0)
        self.g1_main_frame.grid(row=0, column=0, sticky=W + N, padx=10)
        self.g1_button_add_graph = create_button(self.g1_main_frame, "pridaj G1", 0,0)
        self.g1_button_add_2factors = create_button(self.g1_main_frame, "pridaj G1 2-faktor", 1, 0)
        self.g1_combo_box = create_combo_box(self.g1_main_frame,2,0)
        self.g1_scrollbar_wrapper = create_scrollbar_frame(self.g1_main_frame,4,0)

        self.g1_button_add_graph.config(bootstyle="info")
        self.g1_button_add_2factors.config(bootstyle="info")
        # disable veci, ktore budu dostupne az po nahrati grafu
        self.g1_button_add_2factors.config(state=DISABLED)
        self.g1_combo_box.config(state=DISABLED)

        bind_function_to_button(self.g1_button_add_graph, partial(self.function_create_graph_from_file, self.G1, self.g1_scrollbar_wrapper, self.g1_array_of_labels))
        bind_function_to_button(self.g1_button_add_2factors, partial(self.function_load_2factors_from_file,self.G1, self.g1_combo_box, self.g1_array_of_labels))
        bind_function_to_combo_box(self.g1_combo_box, partial(self.function_selected_2factor, graph = self.G1, array_of_labels = self.g1_array_of_labels))

    # funkcia vytvori zakladne widgety pre graf G2
    def create_g2_widgets(self):
        self.g2_main_frame = create_frame(self, 0, 1)
        self.g2_main_frame.grid(row=0, column=1, sticky=W + N, padx=(50))
        self.g2_button_add_graph = create_button(self.g2_main_frame, "pridaj G2", 0,0)
        self.g2_button_add_2factors = create_button(self.g2_main_frame, "pridaj G1 2-faktor", 1, 0)
        self.g2_combo_box = create_combo_box(self.g2_main_frame,2,0)
        self.g2_scrollbar_wrapper = create_scrollbar_frame(self.g2_main_frame,4,0)

        self.g2_button_add_graph.config(bootstyle="info")
        self.g2_button_add_2factors.config(bootstyle="info")

        bind_function_to_button(self.g2_button_add_graph, partial(self.function_create_graph_from_file, self.G2, self.g2_scrollbar_wrapper, self.g2_array_of_labels))
        bind_function_to_button(self.g2_button_add_2factors, partial(self.function_load_2factors_from_file,self.G2, self.g2_combo_box, self.g2_array_of_labels))
        bind_function_to_combo_box(self.g2_combo_box, partial(self.function_selected_2factor, graph = self.G2, array_of_labels=self.g2_array_of_labels))

        # disable veci, ktore budu dostupne az po nahrati grafu
        self.g2_button_add_2factors.config(state=DISABLED)
        self.g2_combo_box.config(state=DISABLED)

    # funkcia vytvori zakladne widgety pre graf G3
    def create_g3_widgets(self):
        self.g3_main_frame = create_frame(self, 0, 2)
        self.g3_main_frame.grid(row=0, column=2, sticky=W + N, padx=(50))
        self.result_button = create_button(self.g3_main_frame, "Vytvor", 0, 0)
        self.result_all_button = create_button(self.g3_main_frame, "Vytvor všetko", 1, 0)
        self.g3_scrollbar_wrapper = create_scrollbar_frame(self.g3_main_frame, 3,0)

        self.result_button.config(bootstyle="info")
        self.result_all_button.config(bootstyle="info")

    # funkcia nacita graf zo subora
    def function_create_graph_from_file(self, graph, scrollbar_wrapper, array_of_labels):
        file_name = filedialog.askopenfilename(title="Vyberte graf", filetypes=(("txt súbory", "*.txt"), ("všetky súbory files", "*.*")))
        if self.check_graph_file(file_name) is False:
            return False
        self.handle_adding_new_graph(graph)
        graph.create_graph_from_file(file_name)
        self.create_graph_visualization(graph, scrollbar_wrapper, array_of_labels)
        self.enable_2factor_widgets_for_graph(graph)
        self.handle_setting_cursor_for_labels()
        return True

    def check_graph_file(self, filename):
        if filename is "":
            return False
        f = open(filename, "r")
        first_row = f.readline()

        # kontrolujem ci v prvom riadku je jedno cislo
        if not first_row.strip().isdigit():
            messagebox.showerror('CHYBA', 'Zlý formát grafu')
            return False
        number_of_verticies = int(first_row)

        # kontrolujem ci pocet vrcholov je viac ako 0
        if number_of_verticies <= 0:
            messagebox.showerror('CHYBA', 'Zlý formát grafu')
            return False

        for i in range(number_of_verticies):
            three_verticies = f.readline().split()

            # kontrolujem ci v kazdom riadku pre vrchol sú 3 vrcholy
            if len(three_verticies) != 3:
                messagebox.showerror('CHYBA', 'Zlý formát grafu')
                return False

            # kontrolujem ci kazdy z vrcholov je cislo mensie ako pocet vrcholov
            for vertex in three_verticies:
                if (not vertex.isdigit()) or int(vertex) >= number_of_verticies:
                    messagebox.showerror('CHYBA', 'Zlý formát grafu')
                    return False
        f.close()
        return True

    def handle_adding_new_graph(self, graph):
        if graph is self.G1:
            self.reset_g1_adding()
        elif graph is self.G2:
            self.reset_g2_adding()

    # funkcia riesi ci chcem nastavit kursor na hand2, nastavuje sa podla potomka tejto triedy
    def handle_setting_cursor_for_labels(self):
        pass

    # doplnenie toho, ze spristupnim veci pre graf, ktory som nahral
    def enable_2factor_widgets_for_graph(self, graph):
        if graph is self.G1:
            if self.g1_button_add_2factors.winfo_exists():
                self.g1_button_add_2factors.config(state=NORMAL)
            if self.g1_combo_box.winfo_exists():
                self.g1_combo_box.config(state=NORMAL)
        elif graph is self.G2:
            self.g2_button_add_2factors.config(state=NORMAL)
            self.g2_combo_box.config(state=NORMAL)

    # funkcia nacita graf na obrazovku
    def create_graph_visualization(self, graph, scrollbar_wrapper, array_of_labels):
        adjacency_list = graph.adjacency_list

        scrollbar = scrollbar_wrapper.scrollbar
        canvas = scrollbar_wrapper.canvas
        frame_in_canvas = scrollbar_wrapper.frame_in_canvas

        self.create_clickable_labels_in_frame(adjacency_list, frame_in_canvas, array_of_labels)

        frame_in_canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        self.update()
        #canvas.config(width=200 - scrollbar.winfo_width())

    def add_spaces_before_number(self, number):
        if number < 10:
            return "  "+str(number)
        elif number < 100:
            return " "+str(number)
        return str(number)

    # funkcia vytvori pre graf labely, na ktore sa da klikat
    def create_clickable_labels_in_frame(self, adjacency_list, frame, array_of_labels):
        for i in range(len(adjacency_list)):
            Label(text=self.add_spaces_before_number(i) + ": ", master=frame, font="TkDefaultFont 11").grid(row=i, column=0, sticky=W, pady=2,padx=2)

            new_array = []
            label1 = self.create_clickable_label(i, adjacency_list[i][0], frame, 1)
            label2 = self.create_clickable_label(i, adjacency_list[i][1], frame, 2)
            label3 = self.create_clickable_label(i, adjacency_list[i][2], frame, 3)
            new_array.extend([label1, label2, label3])
            array_of_labels.append(new_array)

    # funkcia vytvori jeden potrebny hranovy label a nabinduje mu prislusnu funkciu
    def create_clickable_label(self, vertex1, vertex2, frame, column):
        label = create_highligted_label(frame, self.add_prefix_space(vertex2), "white", row=vertex1, column=column)
        if frame is self.g1_scrollbar_wrapper.frame_in_canvas:
            bind_function_to_label(label, partial(self.g1_switch_selected_edge, vertex1=vertex1, vertex2=vertex2, label=label))
        elif frame is self.g2_scrollbar_wrapper.frame_in_canvas:
            bind_function_to_label(label, partial(self.g2_switch_selected_edge, vertex1=vertex1, vertex2=vertex2, label=label))
        return label

    # pomocna funkcia pre pridavanie medzier
    def add_prefix_space(self, number):
        if number < 10:
            return "  " + str(number) + "  "
        if number < 100:
            return " " + str(number) + " "
        return str(number)

    def check_2factor_file(self, file_name, graph):
        if file_name is "":
            return False
        file = open(file_name, "r")
        number = file.readline()  # precitaj pocet 2factorov

        # kontrolujem ci prvy riadok obsahuje iba jedno cislo
        if not number.strip().isdigit():
            messagebox.showerror('CHYBA', 'Zlý formát 2-faktorov')
            return False
        number = int(number.strip())

        # kontrolujem, ci v subore je aspon 1 2-faktor
        if number <= 0:
            messagebox.showerror('CHYBA', 'Zlý formát 2-faktorov')
            return False

        for i in range(number):
            number1 = file.readline()

            # kontrolujem ci je najprv poradie ako nejake cislo
            if not number1.strip().isdigit():
                messagebox.showerror('CHYBA', 'Zlý formát 2-faktorov')
                return False
            size = file.readline()

            # kontrolujem ci velkost cyklov je cislo
            if not size.strip().isdigit():
                messagebox.showerror('CHYBA', 'Zlý formát 2-faktorov')
                return False
            size = int(size)

            # kontrolujem ci sa zhoduje velkost cyklov s poctom vrcholov grafu
            if len(graph.adjacency_list) != 2*size:
                messagebox.showerror('CHYBA', '2-faktory nepatria ku grafu')
                return False

            row1 = file.readline().split()
            # kontrolujem ci sedi velkost prveho cyklu
            if len(row1) != size:
                messagebox.showerror('CHYBA', 'Zlý formát 2-faktorov')
                return False
            row1_int = []

            # kontrolujem ci kazdy element v cykle je cislo mensie ako dlzka cyklu krat 2
            for vertex in row1:
                if (not vertex.isdigit()) or int(vertex) >= size*2:
                    messagebox.showerror('CHYBA', 'Zlý formát 2-faktorov')
                    return False
                row1_int.append(int(vertex))

            # kontrolujem ci prvy cyklus je vobec v grafe
            if self.is_cycle_in_graph(graph, row1_int) == False:
                messagebox.showerror('CHYBA', '2-faktory nepatria ku grafu')
                return False

            row2 = file.readline().split()
            # kontrolujem ci sedi velkost druheho cyklu
            if len(row2) != size:
                messagebox.showerror('CHYBA', 'Zlá formát 2-faktorov')
                return False
            row2_int = []

            # kontrolujem ci kazdy element v cykle je cislo mensie ako dlzka cyklu krat 2
            for vertex in row2:
                if (not vertex.isdigit()) or int(vertex) >= size*2:
                    messagebox.showerror('CHYBA', 'Zlý formát 2-faktorov')
                    return False
                row2_int.append(int(vertex))

            # kontrolujem ci druhy cyklus je vobec v grafe
            if self.is_cycle_in_graph(graph, row2_int) == False:
                messagebox.showerror('CHYBA', '2-faktory nepatria ku grafu')
                return False

            # kontrolujem ci 2faktor je korektny, to znamena ci kazdy vrchol o 0 po n-1 je prave v jednom z cyklov
            if self.is_correct_2factor(2*size, row1_int, row2_int) == False:
                messagebox.showerror('CHYBA', 'Zlý 2-faktor')
                return False

        file.close()
        return True

    # funkcia skontroluje ci v grafe sa nachadza cyklus
    def is_cycle_in_graph(self, graph, cycle):
        for i in range(len(cycle)-1):
            if cycle[i] not in graph.adjacency_list[cycle[i+1]]:
                return False
        if cycle[-1] not in graph.adjacency_list[cycle[0]]:
            return False
        return True

    # funkcia skontoluje, ci je to korektny perm 2-cyklus, cize ci kazdy vertex je prave v jednom z cyklov
    def is_correct_2factor(self, size, cycle1, cycle2):
        for i in range(size):
            # i sa nachadza v oboch perm cykloch
            if i in cycle1 and i in cycle2:
                return False
            # i sa nenachadza ani v jednom perm cykle
            if not (i in cycle1 or i in cycle2):
                return False
        return True

    # funkcia ohandluje nacitanie 2 faktorov
    def function_load_2factors_from_file(self, graph, combo_box, array_of_labels, filter_involution_2_factors = False):
        file_name = filedialog.askopenfilename(title="Vyberte 2faktory", filetypes=(("txt súbory", "*.txt"), ("všetky súbory files", "*.*")))
        if self.check_2factor_file(file_name, graph) is False:
            return
        array_of_2factors = self.read_file_of_2factors(file_name, graph, filter_involution_2_factors)
        if len(array_of_2factors) == 0:
            messagebox.showerror('CHYBA', 'V súbore nie je žiaden vyhovujúci 2-faktor')
            return
        self.reset_after_loading_file_of_2facrors(graph)
        array_of_values = []
        for i in range(len(array_of_2factors)):
            array_of_values.append(str(i + 1 ))
        combo_box["values"] = array_of_values
        combo_box.current(0)
        graph.twoFactors.extend(array_of_2factors)
        self.highlight_2factor_of_graph(graph, graph.twoFactors[0], array_of_labels)
        graph.selected_2factor = graph.twoFactors[0]

    # resetujem predtym ako nacitam subor 2faktorov
    def reset_after_loading_file_of_2facrors(self, graph):
        if graph is self.G1:
            self.reset_g1_adding_2factor()
        elif graph is self.G2:
            self.reset_g2_adding_2factor()

    # precita 2faktory zo subora a vrati zoznam 2faktorov
    def read_file_of_2factors(self, file_name, graph, filter_involution_2_factors = False):
        file = open(file_name, "r")
        number = int(file.readline())  # precitaj pocet 2factorov
        twoFactors = []
        for i in range(number):
            file.readline()
            file.readline()
            newTwoFactor = TwoFactor([int(i) for i in file.readline().split()],[int(i) for i in file.readline().split()])
            twoFactors.append(newTwoFactor)
        file.close()
        if filter_involution_2_factors:
            twoFactors = self.get_involution_2_factors(graph, twoFactors)
        return twoFactors

    # funkcia vrati pole, kde budu iba involucne 2faktory, ostatne zahodi
    def get_involution_2_factors(self, graph, twoFactors):
        for i in range(len(twoFactors) - 1, -1, -1):
            if graph.get_first_involution_for_2factor(twoFactors[i]) is None:
                twoFactors.pop(i)
        return twoFactors

    # funkcia zvyrazni 2faktor
    def highlight_2factor_of_graph(self, graph, twoFactor, edge_labels):
        self.unhiglight_2_factor_of_graph(edge_labels)
        cycle1 = twoFactor.cycle1
        cycle2 = twoFactor.cycle2

        adjacency_list = graph.adjacency_list
        for i in range(len(adjacency_list)):
            for j in range(len(adjacency_list[i])):
                vertex = adjacency_list[i][j]
                if vertex in cycle1 and i in cycle1:
                    edge_labels[i][j].config(fg="white", bg ="#D70040")
                elif vertex in cycle2 and i in cycle2:
                    edge_labels[i][j].config(fg="white", bg="#6495ED")

    # v danom grafe G odvyrazni hociaky 2faktor bol pouzity
    def unhiglight_2_factor_of_graph(self, edge_labels):
        for i in range(len(edge_labels)):
            for j in range(len(edge_labels[i])):
                edge_labels[i][j].config(bg="white", fg="black")

    # funkcia, ktora sa zavola po vybrati z combolistu pre 2faktory
    def function_selected_2factor(self, event, graph, array_of_labels):
        index = int(event.widget.get()) - 1
        self.highlight_2factor_of_graph(graph, graph.twoFactors[index], array_of_labels)
        graph.selected_2factor = graph.twoFactors[index]

        # vykonam potrebne zmeny podla toho, pre ktory graf som zmenil 2faktor
        if graph is self.G1:
            self.reset_g1_adding_2factor()
        elif graph is self.G2:
            self.reset_g2_adding_2factor()

    # funkcia, ktora sa vykona po kliknuti na label pre g1 hrany
    def g1_switch_selected_edge(self, event, vertex1, vertex2, label):
        pass

    # funkcia, ktora sa vykona po kliknuti na label pre g2 hrany
    def g2_switch_selected_edge(self, event, vertex1, vertex2, label):
        pass

    def write_g3_to_frame(self):
        self.create_graph_visualization(self.G3, self.g3_scrollbar_wrapper, [])

    # funkcia, ktora sa zavola po kliknuti na vertex label pri selection
    def handle_click_on_selection_label(self, event, left_side_labels):
        label = event.widget
        color = label.cget("background")

        if self.selected_selection_lbl is None:
            if label in left_side_labels:
                self.selected_selection_lbl = label
                #label.config(bg=color, fg="white")
                label.config(relief="solid")
                return
            return

        if label in left_side_labels:
            #self.selected_selection_lbl.config(bg="white", fg="black")
            self.selected_selection_lbl.config(relief="flat")
            self.selected_selection_lbl = label
            #label.config(bg=color, fg="white")
            label.config(relief="solid")
            return

        self.do_correct_connections(self.selected_selection_lbl, label)
        #self.selected_selection_lbl.config(bg="white", fg="black")
        self.selected_selection_lbl.config(relief="flat")
        self.selected_selection_lbl = None

    # vrati ci je zvoleny label reprezentuje priecku
    def label_is_spoke(self, label):
        return label.cget("bg") == "white"

    # vrati ci 2 labely maju rovnaku farbu
    def labels_have_same_color(self, label1, label2):
        return label1.cget("bg") == label2.cget("bg")

    # funkcia, ktora vyriesi zobrazenie po tom co zmenime 2faktor pre g1
    def reset_g1_adding_2factor(self):
        pass

    # funkcia, ktora vyriesi zobrazenie po tom co zmenime 2faktor pre g2
    def reset_g2_adding_2factor(self):
        pass

    def reset_g1_adding(self):
        # resetnem graf G1
        self.G1.reset_graph()

        # odstavim vsetko co by sa malo nastavit, uz pri zmene 2faktora
        self.reset_g1_adding_2factor()

        # vypraznim pole labelov
        self.g1_array_of_labels.clear()

        # combo box musim vynulovat
        if self.g1_combo_box.winfo_exists():
            self.g1_combo_box["values"] = []
            self.g1_combo_box.set("")

        # vyprazdnim vizualizaciu
        frame = self.g1_scrollbar_wrapper.frame_in_canvas
        for widget in frame.winfo_children():
            widget.destroy()



    def reset_g2_adding(self):
        # resetnem graf G1
        self.G2.reset_graph()

        # odstavim vsetko co by sa malo nastavit, uz pri zmene 2faktora
        self.reset_g2_adding_2factor()

        # vypraznim pole labelov
        self.g2_array_of_labels.clear()

        # combo box musim vynulovat
        self.g2_combo_box["values"] = []
        self.g2_combo_box.set("")

        # vyprazdnim vizualizaciu
        frame = self.g2_scrollbar_wrapper.frame_in_canvas
        for widget in frame.winfo_children():
            widget.destroy()

    # vytvori combo boxy na vyberanie konkretnych involucii
    def create_inv_combo_boxes(self):
        self.combo_box_g1_inv = create_combo_box(self.g1_main_frame, 3, 0)
        self.combo_box_g2_inv = create_combo_box(self.g2_main_frame, 3, 0)
        self.combo_box_g1_inv.config(width=15)
        self.combo_box_g2_inv.config(width=15)
        bind_function_to_combo_box(self.combo_box_g1_inv, partial(self.change_involution_from_combo_box, graph=self.G1))
        bind_function_to_combo_box(self.combo_box_g2_inv, partial(self.change_involution_from_combo_box, graph=self.G2))

    def change_involution_from_combo_box(self, e, graph):
        pass

    def create_values_for_inv_combo_box(self, involutions):
        array = []
        for i in involutions:
            string = "(" + str(i[0][0]) + " " +str(i[0][1]) +") ("+ str(i[1][0]) + " " + str(i[1][1]) + ")"
            array.append(string)
        return array






