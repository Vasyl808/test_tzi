import os
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, simpledialog

from loading_window import LoadingWindowHash
from main_page import MainAppPage
from write_to_file import WriteToFile


class HashApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(MainAppPage))
        button.grid(row=0, column=1, pady=10, padx=10, sticky="nw")

        verify_button1 = tk.Button(self, text="Hash string",
                                   command=lambda: self.controller.show_frame(StringHashPage))
        verify_button1.grid(row=1, column=3, padx=(120, 0), pady=10)
        verify_button2 = tk.Button(self, text="Hash file",
                                   command=lambda: self.controller.show_frame(FileHashPage))
        verify_button2.grid(row=2, column=3, padx=(120, 0), pady=10)

        verify_button = tk.Button(self, text="Verify File Integrity",
                                  command=lambda: self.controller.show_frame(VerifyIntegrityPage))
        verify_button.grid(row=3, column=3, padx=(120, 0), pady=10)


class VerifyIntegrityPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.file1 = None
        self.file2 = None
        button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(HashApp))
        button.grid(row=0, column=1, pady=10, padx=10, sticky="nw")

        self.file_name_entry1 = tk.Entry(self, width=40)
        self.file_name_entry1.grid(row=1, column=1, pady=5, padx=(100, 0), sticky="w")
        self.file_name_entry1.config(state="readonly", exportselection=1)

        clear1 = tk.Button(self, text="Clear", command=self.clear_f1)
        clear1.grid(row=1, column=1, pady=5, padx=(350, 0))

        select1 = tk.Button(self, text="Select the file to check", command=self.select_file1)
        select1.grid(row=2, column=1, pady=5, padx=(70, 0))

        self.file_name_entry2 = tk.Entry(self, width=40)
        self.file_name_entry2.grid(row=3, column=1, pady=5, padx=(100, 0), sticky="w")
        self.file_name_entry2.config(state="readonly", exportselection=1)

        clear2 = tk.Button(self, text="Clear", command=self.clear_f2)
        clear2.grid(row=3, column=1, pady=5, padx=(350, 0))

        select2 = tk.Button(self, text="Select the file with the hash \n (only in txt format)",
                            command=self.select_file2)
        select2.grid(row=4, column=1, pady=5, padx=(70, 0))

        label3 = tk.Label(self, text="File integrity:")
        label3.grid(row=5, column=1, pady=20, padx=(80, 0), sticky="nw")

        self.label4 = tk.Label(self, width=30, text="Here you can see your result")
        self.label4.grid(row=5, column=1, padx=(150, 0), )

        verify_button = tk.Button(self, text="Verify File Integrity", command=self.verify_integrity)
        verify_button.grid(row=7, column=1, padx=(70, 0), pady=5)

    def clear_f1(self):
        if self.file1:
            self.label4.config(text="Here you can see your result")
            self.file1 = None
            self.file_name_entry1.config(state="normal", exportselection=1)
            self.file_name_entry1.delete(0, "end")
            self.file_name_entry1.config(state="readonly", exportselection=1)

    def clear_f2(self):
        if self.file2:
            self.label4.config(text="Here you can see your result")
            self.file2 = None
            self.file_name_entry2.config(state="normal", exportselection=1)
            self.file_name_entry2.delete(0, "end")
            self.file_name_entry2.config(state="readonly", exportselection=1)

    def select_file1(self):
        file_path = tk.filedialog.askopenfilename()  # Prompt user to select a file
        if file_path:
            max_file_size_mb = 5
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            if file_size_mb <= max_file_size_mb:
                self.file_name_entry1.config(state="normal", exportselection=1)
                self.file_name_entry1.delete(0, "end")
                self.file_name_entry1.insert(tk.END, file_path)
                self.file_name_entry1.config(state="readonly", exportselection=1)
                self.file1 = file_path
            else:
                messagebox.showerror("Error",
                                     f"File size {file_path} ({file_size_mb} MB) exceeds {max_file_size_mb} "
                                     f"MB. The file is too large.")

    def select_file2(self):
        file_path = tk.filedialog.askopenfilename()  # Prompt user to select a file
        if file_path:
            max_file_size_mb = 5
            file_extension = os.path.splitext(file_path)[-1]
            if file_extension == ".txt":
                file_size = os.path.getsize(file_path)
                file_size_mb = file_size / (1024 * 1024)
                if file_size_mb <= max_file_size_mb:
                    self.file_name_entry2.config(state="normal", exportselection=1)
                    self.file_name_entry2.delete(0, "end")
                    self.file_name_entry2.insert(tk.END, file_path)
                    self.file_name_entry2.config(state="readonly", exportselection=1)
                    self.file2 = file_path
                else:
                    messagebox.showerror("Error",
                                         f"File size {file_path} ({file_size_mb} MB)"
                                         f" exceeds {max_file_size_mb} MB. The file is too large.")
            else:
                messagebox.showerror("Error", "You can use only txt file")

    def verify_integrity(self):
        if self.file1 and self.file2:
            loading = LoadingWindowHash(self, file=self.file1)
            loading.wait_window()
            if loading.md5_hash and loading.md5_hash_lib:
                file_hash = loading.md5_hash
            else:
                messagebox.showerror("Error", "Something went wrong! Please try again.")
                return
            try:
                with open(self.file2, "r") as hash_file:
                    stored_hash = hash_file.read()
                if file_hash == str(stored_hash):
                    self.label4.config(text="File integrity verified: The hashes match.")
                else:
                    self.label4.config(text="File integrity check failed: \n The hashes do not match.")
            except FileNotFoundError:
                self.label4.config(text="No hash file found. Please hash the file first.")
        else:
            messagebox.showerror("Error", "Please select two files to check!")


class StringHashPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.hash = None

        button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(HashApp))
        button.grid(row=0, column=1, pady=10, padx=10, sticky="nw")

        label = tk.Label(self, text="Please, input a string to hash:")
        label.grid(row=1, column=1, padx=(100, 5))

        self.input_text = scrolledtext.ScrolledText(self, width=30, height=10, exportselection=1)
        self.input_text.grid(row=2, column=1, padx=(100, 5))

        md5_button = tk.Button(self, text="Compute MD5", command=self.calculate_md5)
        md5_button.grid(row=3, column=1, padx=(60, 0), pady=10)

        save_button = tk.Button(self, text="Save to file", command=self.save)
        save_button.grid(row=3, column=1, padx=(250, 0), pady=10)

        clear_button = tk.Button(self, text="Clear", command=self.clear_hash_value)
        clear_button.grid(row=3, column=1, padx=(120, 0), sticky="nw", pady=10)

        label1 = tk.Label(self, text="Hash value:")
        label1.grid(row=4, column=1, padx=(70, 0), sticky="nw", pady=10)

        self.hash_value = tk.Entry(self, width=40)
        self.hash_value.grid(row=4, column=1, padx=(150, 0), pady=10)

        label2 = tk.Label(self, text="Hash value using library:")
        label2.grid(row=5, column=1, padx=(1, 0), sticky="nw", pady=10)

        self.hash_value_library = tk.Entry(self, width=40)
        self.hash_value_library.grid(row=5, column=1, padx=(150, 0), pady=10)

        self.hash_value.config(state="readonly", exportselection=1)
        self.hash_value_library.config(state="readonly", exportselection=1)

    def calculate_md5(self):
        self.hash_value.config(state="normal", exportselection=1)
        self.hash_value_library.config(state="normal", exportselection=1)
        self.hash_value.delete(0, "end")
        self.hash_value_library.delete(0, "end")
        if len(str(self.input_text.get("1.0", "end-1c"))) > 10 ** 6:
            messagebox.showerror("Error", "The maximum text size should not exceed 10^6 characters")
            return
        input_text = str(self.input_text.get("1.0", "end-1c")).encode()
        loading = LoadingWindowHash(self, data=input_text)
        loading.wait_window()
        if loading.md5_hash and loading.md5_hash_lib:
            self.hash_value.insert(tk.END, f"{loading.md5_hash}")
            self.hash_value_library.insert(tk.END, f"{loading.md5_hash_lib}")
            self.hash = loading.md5_hash
            self.hash_value.config(state="readonly", exportselection=1)
            self.hash_value_library.config(state="readonly", exportselection=1)
        else:
            messagebox.showerror("Error", "Something went wrong! Please try again.")

    def clear_hash_value(self):
        self.hash_value.config(state="normal", exportselection=1)
        self.hash_value_library.config(state="normal", exportselection=1)
        self.hash_value.delete(0, "end")
        self.hash_value_library.delete(0, "end")
        self.input_text.delete(1.0, "end")
        self.hash = None
        self.hash_value.config(state="readonly", exportselection=1)
        self.hash_value_library.config(state="readonly", exportselection=1)

    def save(self):
        if self.hash:
            filename = simpledialog.askstring("Input", "Please, enter a file name to save your hash "
                                                       "(Enter a name without a file extension):")
            if filename:
                if len(str(filename)) > 250:
                    messagebox.showerror("Error", "Invalid filename."
                                        "The maximum possible length of the file name should not exceed 250 characters")
                    return
                try:
                    WriteToFile.save_hash_to_file(str(self.hash), str(filename))
                except Exception as e:
                    messagebox.showerror("Error", "Invalid filename.")
        else:
            messagebox.showerror("Error", "You haven't hashed the string yet! Please, enter a string and hash it")


class FileHashPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.file = None
        self.is_hash = False

        button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(HashApp))
        button.grid(row=0, column=1, pady=10, padx=10, sticky="nw")
        file_hash = tk.Label(self, text="Hash the file")
        file_hash.grid(row=5, column=1, padx=(70, 0), pady=5)

        self.file_name_entry = tk.Entry(self, width=55)
        self.file_name_entry.grid(row=6, column=1, padx=(50, 0))
        self.file_name_entry.config(state="readonly", exportselection=1)

        select = tk.Button(self, text="Select a File", command=self.select_file)
        select.grid(row=7, column=1, padx=(50, 0), sticky="nw", pady=10)

        delete = tk.Button(self, text="Clear", command=self.delete_file)
        delete.grid(row=7, column=1, padx=(160, 0), sticky="nw", pady=10)

        hash_file = tk.Button(self, text="Hash", command=self.hash_file)
        hash_file.grid(row=7, column=1, padx=(230, 0), sticky="nw", pady=10)

        save = tk.Button(self, text="Save hash to file", command=self.save)
        save.grid(row=7, column=1, padx=(300, 0), sticky="nw", pady=10)

        label3 = tk.Label(self, text="Hash value:")
        label3.grid(row=8, column=1, pady=20, padx=(70, 0), sticky="nw")

        self.hash_value = tk.Entry(self, width=40)
        self.hash_value.grid(row=8, column=1, padx=(150, 0))

        label4 = tk.Label(self, text="Hash value using library:")
        label4.grid(row=9, column=1, padx=(1, 0), sticky="nw")

        self.hash_value_library = tk.Entry(self, width=40)
        self.hash_value_library.grid(row=9, column=1, padx=(150, 0))

        self.hash_value.config(state="readonly", exportselection=1)
        self.hash_value_library.config(state="readonly", exportselection=1)

    def clear(self, flag=False):
        if not flag:
            self.file_name_entry.config(state="normal", exportselection=1)
            self.file_name_entry.delete(0, "end")
        self.hash_value.config(state="normal", exportselection=1)
        self.hash_value_library.config(state="normal", exportselection=1)
        self.hash_value.delete(0, "end")
        self.hash_value_library.delete(0, "end")

    def make_readonly(self, flag=False):
        if not flag:
            self.file_name_entry.config(state="readonly", exportselection=1)
        self.hash_value.config(state="readonly", exportselection=1)
        self.hash_value_library.config(state="readonly", exportselection=1)

    def delete_file(self):
        self.is_hash = False
        self.file = None
        self.clear()
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

    def hash_file(self):
        self.is_hash = False
        if self.file:
            loading = LoadingWindowHash(self, file=self.file)
            loading.wait_window()
            if loading.md5_hash and loading.md5_hash_lib:
                self.clear(flag=True)
                self.hash_value.insert(tk.END, f"{loading.md5_hash}")
                self.hash_value_library.insert(tk.END, f"{loading.md5_hash_lib}")
                self.make_readonly(flag=True)
                self.is_hash = True
            else:
                messagebox.showerror("Error", "Something went wrong! Please try again.")
        else:
            messagebox.showerror("Error", "You have not selected a file! Please select a file!")

    def save(self):
        if self.file and self.is_hash:
            filename = simpledialog.askstring("Input", "Enter the name of the file "
                                                       "(Enter a name without a file extension):")
            if filename:
                try:
                    WriteToFile.save_hash_to_file(str(self.hash_value.get()), filename)
                except Exception as e:
                    messagebox.showerror("Error", "Invalid filename. Don't use characters like ""\*/:? <> | and spaces")
        else:
            messagebox.showerror("Error", "You have not selected a file! Please select a file!")

