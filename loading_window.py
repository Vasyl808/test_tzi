import hashlib
import queue
import threading
import tkinter as tk
from abc import ABC, abstractmethod

from md5 import MD5Hash
from write_to_file import WriteToFile


class LoadingWindowBase(tk.Toplevel, ABC):
    def __init__(self, parent, title, task_text, on_complete_callback):
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        self.geometry("200x100")
        self.label = tk.Label(self, text=task_text, font=("Helvetica", 12))
        self.label.pack(pady=20)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self.perform_task)
        self.thread.start()
        self.on_complete_callback = on_complete_callback

    def on_close(self):
        if self.thread.is_alive():
            self.thread.join()
        self.withdraw()
        self.destroy()

    def perform_task(self):
        try:
            self.execute_task()
        except Exception as e:
            self.queue.put(None)
        finally:
            self.parent.after(0, self.on_task_complete)

    def on_task_complete(self):
        try:
            result = self.queue.get_nowait()
            if result is not None:
                self.on_complete_callback()
            else:
                self.label.config(text="Error during the task")
        except queue.Empty:
            self.parent.after(100, self.on_task_complete)

    @abstractmethod
    def execute_task(self):
        raise NotImplemented


class LoadingWindow(LoadingWindowBase):
    def __init__(self, parent, generator):
        def on_complete_callback():
            self.generated_numbers = self.generated_data
            self.label.config(text="Generation complete")
            self.on_close()
        self.generator = generator
        self.generated_numbers = None
        self.generated_data = None
        super().__init__(parent, "Wait", "Number generation...", on_complete_callback)

    def execute_task(self):
        self.generated_data = self.generator.generate()
        self.queue.put(self.generated_data)


class SavingWindow(LoadingWindowBase):
    def __init__(self, parent, numbers_to_save):
        def on_complete_callback():
            self.label.config(text="Recording completed")
        self.numbers_to_save = numbers_to_save
        super().__init__(parent, "Wait", "Writing numbers to a file...", on_complete_callback)

    def execute_task(self):
        WriteToFile.write_to_file(numbers=self.numbers_to_save)
        self.queue.put(self.numbers_to_save)


class LoadingWindowHash(LoadingWindowBase):
    def __init__(self, parent, file=None, data=None):
        def on_complete_callback():
            self.on_close()
        self.file = file
        self.data = data
        self.md5_hash_lib = None
        self.md5_hash = None
        self.is_hash = False
        super().__init__(parent, "Wait", "Hashing...", on_complete_callback)

    def execute_task(self):
        if self.file is not None:
            with open(self.file, 'rb') as file:
                data = file.read()
                self.md5_hash_lib = hashlib.md5(data).hexdigest()
                md = MD5Hash()
                self.md5_hash = md.md5(bytearray(data))
                self.is_hash = True
                self.queue.put(self.md5_hash)
        elif self.data is not None:
            self.md5_hash_lib = hashlib.md5(self.data).hexdigest()
            md = MD5Hash()
            self.md5_hash = md.md5(bytearray(self.data))
            self.is_hash = True
            self.queue.put(self.md5_hash)


class CodeWindow(LoadingWindowBase):
    def __init__(self, parent, function, file_in, file_out, text):
        def on_complete_callback():
            self.label.config(text="Recording completed")
        self.function = function
        self.file_in = file_in
        self.file_out = file_out
        self.text = text
        super().__init__(parent, "Wait", self.text, on_complete_callback)

    def execute_task(self):
        result = self.function(self.file_in, self.file_out)
        self.queue.put(result)
