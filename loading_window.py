import hashlib
import queue
import threading
from tkinter import messagebox
import tkinter as tk

from md5 import md5_
from write_to_file import WriteToFile


class LoadingWindow(tk.Toplevel):
    def __init__(self, parent, generator):
        super().__init__(parent)
        self.parent = parent
        self.generator = generator
        self.generated_numbers = None
        self.title("Wait")
        self.geometry("200x100")
        self.label = tk.Label(self, text="Number generation...", font=("Helvetica", 12))
        self.label.pack(pady=20)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.generate_numbers)
        self.thread.start()

    def on_close(self):
        if self.thread.is_alive():
            self.thread.join()
        self.withdraw()
        self.destroy()

    def generate_numbers(self):
        try:
            generated_data = self.generator.generate()
            self.queue.put(generated_data)
        except Exception as e:
            self.queue.put(None)
        finally:
            self.parent.after(0, self.on_generation_complete)

    def on_generation_complete(self):
        try:
            generated_data = self.queue.get_nowait()
            if generated_data is not None:
                self.generated_numbers = generated_data
                self.label.config(text="Generation complete")
                self.on_close()
            else:
                self.label.config(text="Error during generation")
        except queue.Empty:
            # Результат генерації ще не готовий, спробуйте ще раз через короткий інтервал
            self.parent.after(100, self.on_generation_complete)


class SavingWindow(tk.Toplevel):
    def __init__(self, parent, numbers_to_save):
        super().__init__(parent)
        self.parent = parent
        self.numbers_to_save = numbers_to_save
        self.title("Wait")
        self.geometry("200x100")
        self.label = tk.Label(self, text="Writing numbers to a file...", font=("Helvetica", 12))
        self.label.pack(pady=20)
        self.queue = queue.Queue()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.thread = threading.Thread(target=self.save_numbers_to_file)
        self.thread.start()

    def on_close(self):
        if self.thread.is_alive():
            self.thread.join()
        self.withdraw()
        self.destroy()

    def save_numbers_to_file(self):
        try:
            WriteToFile.write_to_file(numbers=self.numbers_to_save)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.label.config(text="Recording completed")
            self.parent.after(0, self.on_complete())

    def on_complete(self):
        try:
            data = self.queue.get_nowait()
            if data is not None:
                self.label.config(text="Recording completed")
            else:
                self.label.config(text="Error")
        except queue.Empty:
            self.parent.after(100, self.on_complete)


class LoadingWindowHash(tk.Toplevel):
    def __init__(self, parent, file=None, data=None):
        super().__init__(parent)
        self.parent = parent
        self.file = file
        self.data = data
        self.md5_hash_lib = None
        self.md5_hash = None
        self.is_hash = False
        self.title("Wait")
        self.geometry("200x100")
        self.label = tk.Label(self, text="Hashing...", font=("Helvetica", 12))
        self.label.pack(pady=20)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.hash_data)
        self.thread.start()

    def on_close(self):
        if self.thread.is_alive():
            self.thread.join()
        self.withdraw()
        self.destroy()

    def hash_data(self):
        if self.file is not None:
            try:
                with open(self.file, 'rb') as file:
                    data = file.read()
                    self.md5_hash_lib = hashlib.md5(data).hexdigest()
                    self.md5_hash = md5_(bytearray(data))
                    self.is_hash = True
                    self.queue.put(self.md5_hash)
            except Exception as e:
                self.queue.put(None)
            finally:
                self.parent.after(0, self.on_hash_complete)
        elif self.data is not None:
            try:
                self.md5_hash_lib = hashlib.md5(self.data).hexdigest()
                self.md5_hash = md5_(bytearray(self.data))
                self.is_hash = True
                self.queue.put(self.md5_hash)
            except Exception as e:
                self.queue.put(None)
            finally:
                self.parent.after(0, self.on_hash_complete)

    def on_hash_complete(self):
        try:
            hash_result = self.queue.get_nowait()
            if hash_result is not None:
                self.on_close()
            else:
                self.label.config(text="Error during hashing")
        except queue.Empty:
            self.parent.after(100, self.on_hash_complete)
