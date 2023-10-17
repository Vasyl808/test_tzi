import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import json
from write_to_file import WriteToFile
from generator import NumberGenerator


class RandomNumberGeneratorApp:
    def __init__(self, root, config_file):
        self.root = root
        self.root.title("Генератор псевдовипадкових чисел")
        self.m = tk.StringVar()
        self.a = tk.StringVar()
        self.c = tk.StringVar()
        self.X0 = tk.StringVar()
        self.config_file = config_file
        self.n = tk.StringVar()
        self.period = tk.StringVar()
        self.show_period = tk.BooleanVar()
        self.save_to_file = tk.BooleanVar()
        self.load_configuration()
        self.create_widgets()

    def clear_all(self):
        self.output_text.delete(1.0, tk.END)

    def load_configuration(self):
        try:
            with open(self.config_file, 'r') as config_file:
                config_data = json.load(config_file)
                self.m = tk.StringVar(value=config_data.get('m'))
                self.a = tk.StringVar(value=config_data.get('a'))
                self.c = tk.StringVar(value=config_data.get('c'))
                self.X0 = tk.StringVar(value=config_data.get('X0'))
        except json.JSONDecodeError as e:
            self.period.set("Помилка у конфігураційному файлі")

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        n_label = ttk.Label(main_frame, text="Кількість чисел:")
        n_label.grid(row=4, column=0, sticky=tk.W)
        n_entry = ttk.Entry(main_frame, textvariable=self.n)
        n_entry.grid(row=4, column=1, padx=5)

        show_period_check = ttk.Checkbutton(main_frame, text="Показувати період", variable=self.show_period)
        show_period_check.grid(row=5, columnspan=2, pady=5)

        save_to_file_check = ttk.Checkbutton(main_frame, text="Зберігати в файл", variable=self.save_to_file)
        save_to_file_check.grid(row=6, columnspan=2, pady=5)

        generate_button = ttk.Button(main_frame, text="Згенерувати", command=self.generate_numbers)
        generate_button.grid(row=7, columnspan=2, pady=10)

        result_label = ttk.Label(main_frame, textvariable=self.period)
        result_label.grid(row=8, columnspan=2, pady=10)

        output_label = ttk.Label(main_frame, text="Згенеровані числа:")
        output_label.grid(row=9, column=0, columnspan=2, pady=(0, 5))
        self.output_text = scrolledtext.ScrolledText(main_frame, width=40, height=10)
        self.output_text.grid(row=10, column=0, columnspan=2)

        clear = ttk.Button(main_frame, text="Очистити", command=self.clear_all)
        clear.grid(row=11, columnspan=2, pady=10)

    def generate_numbers(self):
        m_value = self.m.get()
        a_value = self.a.get()
        c_value = self.c.get()
        X0_value = self.X0.get()
        n_value = self.n.get()
        self.output_text.delete(1.0, tk.END)

        if not all([m_value, a_value, c_value, X0_value, n_value]):
            self.period.set("Будь ласка, заповніть всі поля")
            return

        try:
            m = int(eval(m_value))
            a = int(eval(a_value))
            c = int(eval(c_value))
            X0 = int(eval(X0_value))
            n = int(eval(n_value))
            if n > 10 ** 6:
                self.period.set(f"Перевищено ліміт значень, введіть менше число (не більше 2^31)")
                return
            if n < 0:
                self.period.set(f"Значення кількості не може бути від'ємним значенням")
                return
        except Exception as e:
            self.period.set(f"Введено не коректні дані, кількість повиннна бути цілим числом")
            return

        numbers = NumberGenerator(m, a, c, X0, n)
        result = numbers.generate()

        if self.show_period.get():
            self.period.set(f"Період функції генерації: {result['period']} \n")
        else:
            self.period.set("")

        if self.save_to_file.get():
            if self.show_period.get():
                WriteToFile.write_to_file(numbers=result["sequence"], period=result["period"])
                self.period.set(f"Період функції генерації: {result['period']} \n         Збережено у файл")
            else:
                WriteToFile.write_to_file(numbers=result["sequence"])
                self.period.set("Збережено у файл")

        temp = ''

        for number in result["sequence"][:n]:
            temp += (str(number) + " ")
            if len(temp) > 40:
                self.output_text.insert(tk.END, "\n")
                temp = ""
                temp += (str(number) + " ")
            self.output_text.insert(tk.END, str(number) + " ")

