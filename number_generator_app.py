import json
import tkinter as tk
from tkinter import messagebox, scrolledtext

from generator import NumberGenerator, GeneratorPeriod
from loading_window import SavingWindow, LoadingWindow
from main_page import MainAppPage


class NumberGeneratorApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.period = tk.StringVar()
        self.number = None
        self.save_to_file = False
        self.m = tk.StringVar()
        self.a = tk.StringVar()
        self.c = tk.StringVar()
        self.X0 = tk.StringVar()
        self.load_configuration()
        self.create_widgets()
        self.show_period()

    def show_info_window(self, message):
        info_window = tk.Toplevel(self)
        info_window.title("Information")

        label = tk.Label(info_window, text=message)
        label.pack(padx=20, pady=20)

        ok_button = tk.Button(info_window, text="OK", command=info_window.withdraw)
        ok_button.pack(pady=10)

    def create_widgets(self):
        button = tk.Button(self, text="Back",
                           command=lambda: self.controller.show_frame(MainAppPage))
        button.grid(row=0, column=1, pady=10, padx=10, sticky="nw")

        label = tk.Label(self, text="Count of numbers:")
        label.grid(row=1, column=2, sticky=tk.W, padx=(10, 5))

        self.n = tk.Entry(self, width=10)
        self.n.grid(row=1, column=2, padx=(10, 5))

        generate_button = tk.Button(self, text="Generate", command=self.generate_numbers)
        generate_button.grid(row=1, column=2, padx=(200, 0), pady=5)

        perid_label = tk.Label(self, textvariable=self.period)
        perid_label.grid(row=2, column=2, padx=(10, 5))

        self.result_text = scrolledtext.ScrolledText(self, height=10, width=40, state="disabled", exportselection=1)
        self.result_text.grid(row=3, column=2, pady=5, padx=10)

        # period_button = tk.Button(self, text="Show period", command=self.show_period)
        # period_button.grid(row=5, column=2, pady=5, padx=10)

        save_btn = tk.Button(self, text="Write to file", command=self.save)
        save_btn.grid(row=4, column=2, pady=5, padx=(100, 20))

        clear_button = tk.Button(self, text="Clean", command=self.clear_data)
        clear_button.grid(row=4, column=2, sticky=tk.W, padx=(100, 5))

    def load_configuration(self):
        default_values = {
            'm': 4095,
            'a': 1024,
            'c': 2,
            'X0': 8
        }

        try:
            with open("config.json", 'r') as config_file:
                config_data = json.load(config_file)
                if all(map(lambda x: isinstance(x, int) and x > 0,
                           [config_data['m'], config_data['a'], config_data['c'], config_data['X0']])):
                    self.m = tk.StringVar(value=config_data.get('m', default_values['m']))
                    self.a = tk.StringVar(value=config_data.get('a', default_values['a']))
                    self.c = tk.StringVar(value=config_data.get('c', default_values['c']))
                    self.X0 = tk.StringVar(value=config_data.get('X0', default_values['X0']))
                    if (int(config_data.get('w')) == 16 or int(config_data.get('w')) == 32 or int(config_data.get('w')) == 64)\
                            and (0 <= int(config_data.get('r')) <= 255) and (0 <= int(config_data.get('b')) <= 255):
                        pass
                    else:
                        self.show_info_window(
                            "Error in configuration file, the variable w can be 16, 32 or 64, r and b can be from an interval [0, 255]"
                            ", the program works with default values "
                            "('m': 4095, 'a': 1024, 'c': 2, 'X0': 8 'w': 64, 'r': 16, 'b': 32)")
                else:
                    self.m = tk.StringVar(value=default_values['m'])
                    self.a = tk.StringVar(value=default_values['a'])
                    self.c = tk.StringVar(value=default_values['c'])
                    self.X0 = tk.StringVar(value=default_values['X0'])
                    self.show_info_window("Invalid data entered, all values in the configuration file must be "
                                            "be a positive integer. The program works with default values "
                                             "('m': 4095, 'a': 1024, 'c': 2, 'X0': 8)")
        except:
            self.m = tk.StringVar(value=default_values['m'])
            self.a = tk.StringVar(value=default_values['a'])
            self.c = tk.StringVar(value=default_values['c'])
            self.X0 = tk.StringVar(value=default_values['X0'])
            self.show_info_window("There is no configuration file, the program works with default values "
                                  "('m': 4095, 'a': 1024, 'c': 2, 'X0': 8)")

    def save(self):
        if self.number:
            # WriteToFile.write_to_file(numbers=self.number)
            # messagebox.showinfo("Success", "Data is recorded in a file")
            SavingWindow(self, self.number).wait_window()
        else:
            messagebox.showerror("Error", "The sequence has not yet been generated")

    def generate_numbers(self):
        try:
            try:
                n = int(self.n.get())
                if n <= 0 or n > 10 ** 6 or float(self.n.get()) != n:
                    messagebox.showerror("Error", "The number of numbers must be an integer greater"
                                                  " than 0 and not greater than 10^6")
                    return
            except Exception as e:
                messagebox.showerror("Error", "The number of numbers must be an integer greater"
                                              " than 0 and not greater than 10^6")
                return

            m_value = self.m.get()
            a_value = self.a.get()
            c_value = self.c.get()
            X0_value = self.X0.get()

            try:
                m = int(eval(m_value))
                a = int(eval(a_value))
                c = int(eval(c_value))
                X0 = int(eval(X0_value))
                n = int(self.n.get())
            except Exception as e:
                #messagebox.showerror("Error", "Invalid data entered, all values in the configuration file must be "
                #                              "be a positive integer")
                return

            if float(m_value) != m or float(a_value) != a or float(c_value) != c or float(X0_value) != X0:
                #messagebox.showerror("Error",
                #                     "Invalid data entered, all values in the configuration file must be "
                #                     "be a positive integer")
                return

            if 0 > m or 0 > a or 0 > c or 0 > X0:
                #messagebox.showerror("Error",
                #                     "Invalid data entered, all values in the configuration file must be "
                #                     "be a positive integer")
                return

            generator = NumberGenerator(m, a, c, X0, n)
            loading_window = LoadingWindow(self, generator)
            loading_window.wait_window()
            if loading_window.generated_numbers is not None:
                self.number = loading_window.generated_numbers
                # messagebox.showinfo("Success", "The numbers are generated")
            else:
                messagebox.showerror("Error", "Failed to generate numbers.")
                return

            self.result_text.config(state="normal")
            self.result_text.delete(1.0, "end")
            self.result_text.config(state="disabled")
            self.result_text.config(state="normal")

            temp = ''

            for number in loading_window.generated_numbers:
                temp += (str(number) + " ")
                if len(temp) > 40:
                    self.result_text.insert(tk.END, "\n")
                    temp = ""
                    temp += (str(number) + " ")
                self.result_text.insert(tk.END, str(number) + " ")

            self.result_text.config(state="disabled")
        except ValueError as e:
            messagebox.showerror("Error", "Error in the system")

    def show_period(self):
        # if self.period:
        #    messagebox.showinfo("Generation period", f"Generation period: {self.period}")
        #    return
        m_value = self.m.get()
        a_value = self.a.get()
        c_value = self.c.get()
        X0_value = self.X0.get()

        try:
            m = int(eval(m_value))
            a = int(eval(a_value))
            c = int(eval(c_value))
            X0 = int(eval(X0_value))
        except Exception as e:
            #messagebox.showerror("Error", "Invalid data entered, all values in the configuration file must be "
            #                              "be a positive integer")
            return

        if float(m_value) != m or float(a_value) != a or float(c_value) != c or float(X0_value) != X0:
            #messagebox.showerror("Error",
            #                     "Invalid data entered, all values in the configuration file must be "
            #                     "be a positive integer")
            return

        if 0 > m or 0 > a or 0 > c or 0 > X0:
            #messagebox.showerror("Error",
            #                     "Invalid data entered, all values in the configuration file must be "
            #                     "be a positive integer")
            return

        generator = GeneratorPeriod(m, a, c, X0)
        self.period.set(f"The period of the generation function: {str(generator.get_period())}")

        if not self.period:
            messagebox.showerror("Error", "The sequence has not yet been generated")

    def clear_data(self):
        self.number = None
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, "end")
        self.result_text.config(state="disabled")
