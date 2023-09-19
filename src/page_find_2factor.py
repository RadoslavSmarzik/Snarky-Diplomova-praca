from tkinter import messagebox
from functions import *
from graph import TwoFactor
from page import Page
from z3 import *

# trieda pre hladanie permutacnych 2-faktorov
class Page_find_2factor(Page):

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.g2_main_frame.destroy()
        self.g3_scrollbar_wrapper.main_frame.destroy()
        self.result_all_button.destroy()

        self.g1_button_add_2factors.destroy()
        self.g1_combo_box.destroy()

        self.create_involution_checkbox()
        bind_function_to_button(self.result_button, self.find_2factors)


    def create_involution_checkbox(self):
        self.inv_checbox_var = ttk.BooleanVar(value=False)
        checkbox = ttk.Checkbutton(self.g3_main_frame, text="Iba involučné", variable=self.inv_checbox_var, bootstyle="round-toggle")
        checkbox.grid(row=1, column=0, padx=10)

    def find_2factors(self):
        if self.check_if_you_can_execute() == False:
            return
        twoFactors = self.find_2_factors_by_sat_solver()
        if self.inv_checbox_var.get() == True:
            twoFactors = self.get_involution_2_factors(self.G1, twoFactors)
        self.save_2_factors_to_file(twoFactors)

    # FORMAT VYPISANIA

    def save_2_factors_to_file(self, twoFactors):
        file = filedialog.asksaveasfilename(filetypes=[("txt file", ".txt")], defaultextension=".txt")
        if file is "":
            return
        f = open(file, 'w')

        string = self.string_all_2factors(twoFactors)
        f.write(string)
        f.close()

    def format_string_2factor(self, cycle1, cycle2):
        string = str(len(cycle1)) + "\n"
        for vertex in cycle1:
            string += str(vertex) + " "
        string += "\n"
        for vertex in cycle2:
            string += str(vertex) + " "
        return string

    def string_all_2factors(self, array):
        string = str(len(array)) + "\n"
        for i in range(len(array)):
            string += str(i + 1) + "\n"
            string += self.format_string_2factor(array[i].cycle1, array[i].cycle2) + "\n"
        return string

    # HLADANIE POMOCOU SAT SOLVERU
    def find_2_factors_by_sat_solver(self):
        adj = self.G1.adjacency_list

        # vytvorenie boolean premennych
        boolean_variables = []
        for i in range(len(adj)):
            boolean_variables.append(Bool(i))

        # vytvorenie formul
        # pre kazdy vrchol chcem povedat, ze ak je cerveny, tak prave jeho 2 susedia musia byt cerveny
        # podobne ak je vrchol modry, tak prave 2 jeho susedia musia byt modry

        formulas = []

        # x,y, z su susedia vrchola v
        for i in range(len(adj)):
            v = boolean_variables[i]

            x = boolean_variables[adj[i][0]]  # prvy sused vrchola
            y = boolean_variables[adj[i][1]]  # druhy sused vrchola
            z = boolean_variables[adj[i][2]]  # treti sused vrchola

            formula1 = Implies(v, Or(And(x, y, Not(z)), And(x, Not(y), z), And(Not(x), y, z)))
            formula2 = Implies(Not(v), Or(And(Not(x), Not(y), z), And(Not(x), y, Not(z)),And(x, Not(y), Not(z))))

            formulas.append(formula1)
            formulas.append(formula2)

        s = Solver()
        for f in formulas:
            s.append(f)

        # pomocou SAT solvera najdem vsetky modely
        all_models = self.get_all_models_by_blocking(s)

        # kazdy model zmenim na tuple v ktorej budu 2 array reprezentujuce 2 faktor (ale nie este cyklus, len mnozinu)
        arrays_of_models = self.get_arrays_from_models(all_models, boolean_variables)

        # mnoziny 2faktorov zmenim na cykly
        cycles_of_models = self.get_cycles_from_arrays(arrays_of_models, adj)

        # odfiltrujem 2faktory mensie ako n/2
        cycles_of_models = self.get_cycles_size_k(cycles_of_models, len(adj)/2)

        # z cyklov vytvorim TwoFactor objekty
        twoFactors = self.cycles_to_TwoFactors_objects(cycles_of_models)

        return twoFactors

    def cycles_to_TwoFactors_objects(self, cycles):
        array = []
        for cycle in cycles:
            array.append(TwoFactor(cycle[0], cycle[1]))
        return array


    def get_cycles_size_k(self, cycles, k):
        for i in range(len(cycles) - 1, -1, -1):
            if len(cycles[i][0]) != k or len(cycles[i][0]) != k:
                cycles.pop(i)
        return cycles


    def get_cycles_from_arrays(self, all_arrays, adj):
        cycles = []
        for a in all_arrays:
            cycles.append(self.create_2_factor(a[0], a[1], adj))
        return cycles

    # vrati prvy cyklus, ktory sa z pola da vyskladat
    def create_perm_cycle(self, array, adj):
        cycle = []
        vertex = array[0]
        cycle.append(vertex)
        for i in range(len(array) - 1):
            for j in range(3):
                if adj[vertex][j] in array and adj[vertex][j] not in cycle:
                    vertex = adj[vertex][j]
                    cycle.append(vertex)
        return cycle

    def create_2_factor(self, array1, array2, adj):
        cycle1 = self.create_perm_cycle(array1, adj)
        cycle2 = self.create_perm_cycle(array2, adj)
        return (cycle1, cycle2)

    def model_to_array(self, model, variables):
        red_cycle = []
        blue_cycle = []
        for i in range(len(variables)):
            var = variables[i]
            if model[var] == True:
                red_cycle.append(i)
            elif model[var] == False:
                blue_cycle.append(i)
        return (red_cycle, blue_cycle)

    def get_arrays_from_models(self, models, boolean_variables):
        arrays_of_models = []
        for model in models:
            arrays_of_models.append(self.model_to_array(model, boolean_variables))
        return arrays_of_models

    def get_all_models_by_blocking(self, s):
        all_models = []
        res = s.check()

        while (res == sat):
            m = s.model()
            all_models.append(m)

            block = []
            for var in m:
                block.append(var() != m[var])
            s.add(Or(block))

            block = []
            for var in m:
                block.append(var() == m[var])
            s.add(Or(block))

            res = s.check()

        return all_models

    def get_array_without_element(self, array, element):
        a = copy.deepcopy(array)
        a.remove(element)
        return a

    def check_if_you_can_execute(self):
        if self.G1.adjacency_list is None:
            messagebox.showerror('CHYBA', 'Chyba G1')
            return False
        return True
