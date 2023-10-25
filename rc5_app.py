import json
import json
import os
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog

from loading_window import CodeWindow
from main_page import MainAppPage
from rc5 import RC5


class RC5App(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(MainAppPage))
        button.grid(row=0, column=1, pady=10, padx=10, sticky="nw")

        verify_button1 = tk.Button(self, text="Encode file",
                                   command=lambda: self.controller.show_frame(EncodePage))
        verify_button1.grid(row=1, column=3, padx=(130, 0), pady=10)
        verify_button2 = tk.Button(self, text="Decode file",
                                   command=lambda: self.controller.show_frame(DecodePage))
        verify_button2.grid(row=2, column=3, padx=(130, 0), pady=10)


class EncodePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.file = None
        self.w = None
        self.r = None
        self.b = None

        self.load_configuration()

        button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(RC5App))
        button.grid(row=0, column=1, pady=10, padx=10, sticky="nw")
        input_lable = tk.Label(self, text="Please, input keyword:")
        input_lable.grid(row=1, column=1, padx=(70, 0), pady=5)

        self.password = tk.Entry(self, width=40)
        self.password.grid(row=2, column=1, padx=(70, 0), pady=10)
        self.password.config(exportselection=1)

        file_lable = tk.Label(self, text="Please, select a file:")
        file_lable.grid(row=3, column=1, padx=(60, 0), pady=5)

        self.file_name_entry = tk.Entry(self, width=55)
        self.file_name_entry.grid(row=4, column=1, padx=(60, 0), pady=10)
        self.file_name_entry.config(state="readonly", exportselection=1)

        select = tk.Button(self, text="Select a File", command=self.select_file)
        select.grid(row=5, column=1, padx=(120, 0), sticky="nw", pady=10)

        delete = tk.Button(self, text="Clear", command=self.delete_file)
        delete.grid(row=5, column=1, padx=(70, 0), pady=10)

        encode = tk.Button(self, text="Encode", command=self.__encode)
        encode.grid(row=5, column=1, padx=(200, 0), pady=10)

    def show_info_window(self, message):
        info_window = tk.Toplevel(self)
        info_window.title("Information")

        label = tk.Label(info_window, text=message)
        label.pack(padx=20, pady=20)

        ok_button = tk.Button(info_window, text="OK", command=info_window.withdraw)
        ok_button.pack(pady=10)

    def load_configuration(self):
        default_values = {
            "w": 64,
            "r": 16,
            "b": 32
        }
        try:
            with open("config.json", 'r') as config_file:
                config_data = json.load(config_file)
                if all(map(lambda x: isinstance(x, int),
                           [config_data['m'], config_data['a'], config_data['c'], config_data['X0'], config_data['w'],
                            config_data['r'], config_data['b']])):
                    if (int(config_data.get('w')) == 16 or int(config_data.get('w')) == 32 or int(config_data.get('w')) == 64)\
                            and (0 <= int(config_data.get('r')) <= 255) and (0 <= int(config_data.get('b')) <= 255):
                        self.w = int(config_data['w'])
                        self.r = int(config_data['r'])
                        self.b = int(config_data['b'])
                    else:
                        self.w = int(default_values['w'])
                        self.r = int(default_values['r'])
                        self.b = int(default_values['b'])
                        #self.show_info_window(
                        #    "Error in configuration file, the variable w can be 16, 32 or 64, r and b can be from an interval [0, 255]"
                        #    ", the program works with default values "
                        #    "('m': 4095, 'a': 1024, 'c': 2, 'X0': 8 'w': 64, 'r': 16, 'b': 32)")
                        #return
                else:
                    self.w = int(default_values['w'])
                    self.r = int(default_values['r'])
                    self.b = int(default_values['b'])
        except:
            self.w = int(default_values['w'])
            self.r = int(default_values['r'])
            self.b = int(default_values['b'])
            #self.show_info_window("Error in configuration file, the variable w can be 16, 32 or 64, r and b can be from an interval [0, 255]"
            #                      "/n, the program works with default values "
            #                      "('m': 4095, 'a': 1024, 'c': 2, 'X0': 8 'w': 64, 'r': 16, 'b': 32)")

    def clear(self, flag=False):
        if not flag:
            self.file_name_entry.config(state="normal", exportselection=1)
            self.file_name_entry.delete(0, "end")

    def make_readonly(self, flag=False):
        if not flag:
            self.file_name_entry.config(state="readonly", exportselection=1)

    def delete_file(self):
        self.file = None
        self.clear()
        self.password.delete(0, "end")
        self.make_readonly()

    def select_file(self):
        file_path = tk.filedialog.askopenfilename()
        if file_path:
            max_file_size_mb = 5
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            if file_size_mb <= max_file_size_mb:
                self.clear()
                self.file_name_entry.config(state="normal", exportselection=1)
                self.file_name_entry.insert(tk.END, file_path)
                self.file = file_path
                self.make_readonly()
            else:
                messagebox.showerror("Error",
                                     f"File size {file_path} exceeds {max_file_size_mb} "
                                     f"MB. The file is too large.")

    def __encode(self):
        key = str(self.password.get())
        rc5 = RC5(RC5.get_md5_key(key), self.w, self.r, self.b)
        if self.file:
            file_extension = os.path.splitext(self.file)[1]
            filename = simpledialog.askstring("Input", "Enter the name of the file "
                                                       "(Enter a name without a file extension):")
            if filename:
                try:
                    result = CodeWindow(self, rc5.encode_file, self.file, os.path.join(filename + file_extension),
                                        "Encode file...")
                    result.wait_window()
                except Exception as e:
                    messagebox.showerror("Error", "Invalid filename. Don't use characters like ""\*/:? <> | and spaces")
            else:
                return
        else:
            messagebox.showerror("Error", "You have not selected a file! Please select a file!")

        #rc5.encode_file(filename, os.path.join('encoded_' + filename))
        #rc5.decode_file(filename, os.path.join('decoded_' + filename))


class DecodePage(EncodePage):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        EncodePage.__init__(self, parent, controller)
        encode = tk.Button(self, text="Decode", command=self.__decode)
        encode.grid(row=5, column=1, padx=(200, 0), pady=10)

    def __decode(self):
        key = str(self.password.get())
        rc5 = RC5(RC5.get_md5_key(key), self.w, self.r, self.b)
        if self.file:
            file_extension = os.path.splitext(self.file)[1]
            filename = simpledialog.askstring("Input", "Enter the name of the file "
                                                       "(Enter a name without a file extension):")
            if filename:
                try:
                    result = CodeWindow(self, rc5.decode_file, self.file, os.path.join(filename + file_extension),
                                        "Decode file...")
                    result.wait_window()
                except Exception as e:
                    messagebox.showerror("Error", "Invalid filename. Don't use characters like ""\*/:? <> | and spaces")
            else:
                return
        else:
            messagebox.showerror("Error", "You have not selected a file! Please select a file!")
