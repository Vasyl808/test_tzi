import os

from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import DSA
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, scrolledtext

from Cryptodome.Signature import DSS

from main_page import MainAppPage


class SignMessagePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)  # Configure the main column to expand

        # Back Button
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(MessageSignaturePage))
        back_button.grid(row=0, column=0, pady=5, padx=5, sticky="nw")

        # Private Key Label and Button
        private_key_frame = tk.Frame(self)
        private_key_frame.grid(row=1, column=0, pady=10, padx=10, sticky='ew')
        private_key_frame.grid_columnconfigure(1, weight=1)  # Center the content

        self.private_key_label = tk.Label(private_key_frame, text="No file selected")
        self.private_key_label.grid(row=0, column=1, sticky='w')
        self.load_private_key_button = tk.Button(private_key_frame, text="Load Private Key", command=self.load_private_key)
        self.load_private_key_button.grid(row=0, column=0, sticky='e')

        # Label and Entry for Message Input
        message_input_label = tk.Label(self, text="Enter Message to Sign:")
        message_input_label.grid(row=2, column=0, sticky="w")
        self.message_input = scrolledtext.ScrolledText(self, height=5, width=40)
        self.message_input.grid(row=3, column=0, sticky='ew', padx=20)

        # Button Frame for Sign, Save and Clear
        button_frame = tk.Frame(self)
        button_frame.grid(row=4, column=0, sticky='ew')
        button_frame.grid_columnconfigure([0, 1, 2], weight=1)  # Configure button frame to expand

        # Sign Button
        self.sign_button = tk.Button(button_frame, text="Sign Message", command=self.sign_message)
        self.sign_button.grid(row=0, column=0, pady=5)

        # Save Signature Button
        self.save_signature_button = tk.Button(button_frame, text="Save Signature", command=self.save_signature)
        self.save_signature_button.grid(row=0, column=1, pady=5)

        # Clear Message Button
        clear_message_button = tk.Button(button_frame, text="Clear", command=self.clear_message)
        clear_message_button.grid(row=0, column=2, pady=5)

        # Signature Display Label and Text
        signature_display_label = tk.Label(self, text="Generated Signature:")
        signature_display_label.grid(row=5, column=0, sticky="w")
        self.signature_display = tk.Text(self, height=3, width=40, state=tk.DISABLED)
        self.signature_display.grid(row=6, column=0, sticky='ew', padx=20)

        self.private_key = None

    def load_private_key(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    self.private_key = DSA.import_key(file.read())
                    self.private_key_label.config(text=file_path)
            except ValueError as e:
                messagebox.showerror("Invalid Key Format",
                                     "The selected file does not contain a valid DSA key format.")
            except Exception as e:
                messagebox.showerror("Error", "An unexpected error occurred: " + str(e))

    def sign_message(self):
        if self.private_key is None:
            messagebox.showerror("Error", "Private key not loaded.")
            return

        message = self.message_input.get(1.0, tk.END).strip()
        if not message:
            messagebox.showerror("Error", "No message entered. Please enter a message to sign.")
            return

        try:
            mess_enc = SHA256.new(message.encode('utf-8'))
            sign = DSS.new(self.private_key, 'fips-186-3')
            signature = sign.sign(mess_enc)
            #self.message_input.config(state=tk.DISABLED)
            self.signature_display.config(state=tk.NORMAL)  # Enable temporarily to insert text
            self.signature_display.delete(1.0, tk.END)
            self.signature_display.insert(tk.END, signature.hex())
            self.signature_display.config(state=tk.DISABLED)  # Disable again
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_message(self):
        self.signature_display.config(state=tk.NORMAL)  # Enable the message input field
        self.signature_display.delete(1.0, tk.END)

    def save_signature(self):
        signature = self.signature_display.get(1.0, tk.END).strip()
        if not signature:
            messagebox.showerror("Error", "No signature to save. Please sign a message first.")
            return

        file_path = filedialog.asksaveasfilename()
        if not file_path:
            messagebox.showinfo("Info", "Save cancelled or no file selected.")
            return

        with open(file_path, 'w') as output:
            output.write(signature)
        messagebox.showinfo("Success", "Signature saved successfully.")


class SignFilePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)  # Configure the main column to expand

        # Back Button
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(FileSignaturePage))
        back_button.grid(row=0, column=0, pady=5, padx=5, sticky="nw")

        # Private Key Label and Button
        private_key_frame = tk.Frame(self)
        private_key_frame.grid(row=1, column=0, pady=10, padx=10, sticky='ew')
        private_key_frame.grid_columnconfigure(1, weight=1)  # Center the content

        self.private_key_label = tk.Label(private_key_frame, text="No file selected")
        self.private_key_label.grid(row=0, column=1, sticky='w')
        self.load_private_key_button = tk.Button(private_key_frame, text="Load Private Key", command=self.load_private_key)
        self.load_private_key_button.grid(row=0, column=0, sticky='e')

        # File Selection
        self.file_path_label = tk.Label(self, text="No file selected for signing")
        self.file_path_label.grid(row=2, column=0, sticky='ew', padx=20)

        self.load_file_button = tk.Button(self, text="Load File to Sign", command=self.load_file)
        self.load_file_button.grid(row=3, column=0, pady=5)

        # Signature Display Label and Text
        signature_display_label = tk.Label(self, text="Generated Signature:")
        signature_display_label.grid(row=4, column=0, sticky="w", padx=20)
        self.signature_display = tk.Text(self, height=3, width=40, state=tk.DISABLED)
        self.signature_display.grid(row=5, column=0, sticky='ew', padx=20)

        # Button Frame for Sign and Save
        button_frame = tk.Frame(self)
        button_frame.grid(row=6, column=0, sticky='ew')
        button_frame.grid_columnconfigure([0, 1], weight=1)  # Configure button frame to expand

        # Sign Button
        self.sign_button = tk.Button(button_frame, text="Sign File", command=self.sign_file)
        self.sign_button.grid(row=0, column=0, pady=5)

        # Save Signature Button
        self.save_signature_button = tk.Button(button_frame, text="Save Signature", command=self.save_signature)
        self.save_signature_button.grid(row=0, column=1, pady=5)

        self.private_key = None
        self.file_path = None

    def load_private_key(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    self.private_key = DSA.import_key(file.read())
                    self.private_key_label.config(text=file_path)
            except ValueError as e:
                messagebox.showerror("Invalid Key Format",
                                     "The selected file does not contain a valid DSA key format.")
            except Exception as e:
                messagebox.showerror("Error", "An unexpected error occurred: " + str(e))

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Отримуємо розмір файлу у мегабайтах
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            # Перевіряємо, чи розмір файлу не перевищує 5 МБ
            if file_size_mb > 5:
                messagebox.showerror("Error", "The selected file is too large. Please select a file less than 5 MB.")
                return
            self.file_path = file_path
            self.file_path_label.config(text=file_path)

    def sign_file(self):
        if self.private_key is None:
            messagebox.showerror("Error", "Private key not loaded.")
            return

        if self.file_path is None:
            messagebox.showerror("Error", "No file selected. Please select a file to sign.")
            return

        try:
            with open(self.file_path, 'rb') as file:
                message = file.read()
                mess_enc = SHA256.new(message)
                sign = DSS.new(self.private_key, 'fips-186-3')
                signature = sign.sign(mess_enc)
                self.signature_display.config(state=tk.NORMAL)  # Enable temporarily to insert text
                self.signature_display.delete(1.0, tk.END)
                self.signature_display.insert(tk.END, signature.hex())
                self.signature_display.config(state=tk.DISABLED)  # Disable again
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_signature(self):
        signature = self.signature_display.get(1.0, tk.END).strip()
        if not signature:
            messagebox.showerror("Error", "No signature to save. Please sign a message first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt")])
        if not file_path:
            messagebox.showinfo("Info", "Save cancelled or no file selected.")
            return

        with open(file_path, 'w') as output:
            output.write(signature)
        messagebox.showinfo("Success", "Signature saved successfully.")


class MessageVerifyPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Navigation back button
        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="nw")
        back_button = tk.Button(top_frame, text="Back", command=lambda: controller.show_frame(MessageSignaturePage)) # Replace PreviousPage with the actual previous page class name
        back_button.pack(padx=5, pady=5)

        # Center frame for contents
        center_frame = tk.Frame(self)
        center_frame.grid(row=1, column=0, sticky="nsew")

        # Load Public Key
        self.load_pub_key_button = tk.Button(center_frame, text="Load Public Key", command=self.load_public_key)
        self.load_pub_key_button.grid(row=1, column=0)
        self.public_key_label = tk.Label(center_frame, text="No public key loaded")
        self.public_key_label.grid(row=2, column=0, pady=5)

        # Enter String
        self.string_entry_label = tk.Label(center_frame, text="Enter String for Verification:")
        self.string_entry_label.grid(row=3, column=0)

        # Creating a scrollable Text widget
        self.string_text = scrolledtext.ScrolledText(center_frame, wrap=tk.WORD, width=40,
                                                     height=5)  # You can adjust width and height
        self.string_text.grid(row=4, column=0, pady=5, padx=5)

        # Input Signature
        self.signature_entry_label = tk.Label(center_frame, text="Enter Signature or Load Signature File:")
        self.signature_entry_label.grid(row=5, column=0)
        self.signature_entry = tk.Text(center_frame, width=40, height=3)  # Height is in lines
        self.signature_entry.grid(row=7, column=0, pady=5)
        self.load_signature_file_button = tk.Button(center_frame, text="Load Signature File (.txt only)", command=self.load_signature_file)
        self.load_signature_file_button.grid(row=8, column=0, pady=5)

        # Verify Button
        self.verify_button = tk.Button(center_frame, text="Verify Signature", command=self.verify_signature)
        self.verify_button.grid(row=9, column=0, pady=5)

        # Public key, file path, and signature
        self.public_key = None
        self.signature = None

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        for i in range(1, 9):
            center_frame.grid_rowconfigure(i, pad=5)

    def load_signature_file(self):
        signature_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if signature_file_path:
            with open(signature_file_path, 'r') as file:
                self.signature = file.read().strip()
                if not self.signature:
                    messagebox.showinfo("Empty File",
                                        "The selected file is empty. Please select a file that contains a signature.")
                    return
                self.signature_entry.delete("1.0", tk.END)  # Adjusted for tk.Text widget
                self.signature_entry.insert(tk.END, self.signature)

    def load_public_key(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    self.public_key = DSA.import_key(file.read())
                    self.public_key_label.config(text=file_path)
            except Exception as e:
                messagebox.showerror("Error", "An error occurred while loading the public key: " + str(e))

    def verify_signature(self):
        if self.public_key is None:
            messagebox.showerror("Error", "Public key not loaded.")
            return

        string_to_verify = self.string_text.get("1.0", tk.END).strip()  # Get text from Text widget
        if not string_to_verify:
            messagebox.showerror("Error", "No string entered for verification.")
            return

        signature = self.signature_entry.get("1.0", tk.END).strip()  # Adjusted for tk.Text widget
        if not signature:
            messagebox.showerror("Error", "No signature entered or loaded. Please enter or load a signature.")
            return

        try:
            message = string_to_verify.encode()
            mess_enc = SHA256.new(message)
            verifier = DSS.new(self.public_key, 'fips-186-3')
            verifier.verify(mess_enc, bytes.fromhex(signature))
            messagebox.showinfo("Verification", "The signature is valid.")
        except ValueError:
            messagebox.showerror("Verification Error", "The signature is invalid or corrupted.")
        except Exception as e:
            messagebox.showerror("Error", "An unexpected error occurred: " + str(e))


class FileVerifyPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Верхній рядок для кнопки "Back"
        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="nw")
        back_button = tk.Button(top_frame, text="Back", command=lambda: controller.show_frame(FileSignaturePage))
        back_button.pack(padx=10, pady=10)

        # Використання Frame для центрування вмісту
        center_frame = tk.Frame(self)
        center_frame.grid(row=1, column=0, sticky="nsew")

        # Load Public Key
        self.load_pub_key_button = tk.Button(center_frame, text="Load Public Key", command=self.load_public_key)
        self.load_pub_key_button.grid(row=1, column=0, pady=5)
        self.public_key_label = tk.Label(center_frame, text="No public key loaded")
        self.public_key_label.grid(row=2, column=0, pady=5)

        # Load File
        self.load_file_button = tk.Button(center_frame, text="Load File to Verify", command=self.load_file)
        self.load_file_button.grid(row=3, column=0, pady=5)
        self.file_path_label = tk.Label(center_frame, text="No file selected for verification")
        self.file_path_label.grid(row=4, column=0, pady=5)

        # Input Signature
        self.signature_entry_label = tk.Label(center_frame, text="Enter Signature or Load Signature File:")
        self.signature_entry_label.grid(row=5, column=0, pady=5)
        self.signature_entry = tk.Text(center_frame, width=40, height=3)
        self.signature_entry.grid(row=6, column=0, pady=5)
        self.load_signature_file_button = tk.Button(center_frame, text="Load Signature File (.txt only)",
                                                    command=self.load_signature_file)
        self.load_signature_file_button.grid(row=7, column=0, pady=5)

        # Verify Button
        self.verify_button = tk.Button(center_frame, text="Verify Signature", command=self.verify_signature)
        self.verify_button.grid(row=8, column=0, pady=5)

        self.public_key = None
        self.file_path = None
        self.signature = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        for i in range(1, 9):  # Додавання більших відступів між рядками
            center_frame.grid_rowconfigure(i, pad=1)

    def load_signature_file(self):
        signature_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if signature_file_path:
            if os.path.getsize(signature_file_path) > (5 * 1024 * 1024):
                messagebox.showerror("Error", "The signature file is too large. Please select a file less than 5 MB.")
                return

            with open(signature_file_path, 'r') as file:
                self.signature = file.read().strip()

                if not self.signature:
                    messagebox.showinfo("Empty File",
                                        "The selected file is empty. Please select a file that contains a signature.")
                    return
                else:
                    self.signature_entry.delete("1.0", tk.END)  # Adjusted for tk.Text widget
                    self.signature_entry.insert(tk.END, self.signature)

    def load_public_key(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if os.path.getsize(file_path) > (5 * 1024 * 1024):
                messagebox.showerror("Error", "The public key file is too large. Please select a file less than 5 MB.")
                return

            try:
                with open(file_path, 'rb') as file:
                    self.public_key = DSA.import_key(file.read())
                    self.public_key_label.config(text=file_path)
            except ValueError as e:
                messagebox.showerror("Invalid Key Format",
                                     "The selected file does not contain a valid DSA public key format.")
            except Exception as e:
                messagebox.showerror("Error", "An unexpected error occurred: " + str(e))

    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if os.path.getsize(file_path) > (5 * 1024 * 1024):
                messagebox.showerror("Error", "The selected file is too large. Please select a file less than 5 MB.")
                return

            self.file_path = file_path
            self.file_path_label.config(text=file_path)

    def verify_signature(self):
        if self.public_key is None:
            messagebox.showerror("Error", "Public key not loaded.")
            return

        if self.file_path is None:
            messagebox.showerror("Error", "No file selected for verification.")
            return

        signature = self.signature_entry.get("1.0", tk.END).strip()  # Get text from Text widget
        if not signature:
            messagebox.showerror("Error", "No signature entered or loaded. Please enter or load a signature.")
            return

        try:
            with open(self.file_path, 'rb') as file:
                message = file.read()
                mess_enc = SHA256.new(message)
                verifier = DSS.new(self.public_key, 'fips-186-3')
                verifier.verify(mess_enc, bytes.fromhex(signature))
            messagebox.showinfo("Verification", "The signature is valid.")
        except ValueError:
            messagebox.showerror("Verification Error", "The signature is invalid or corrupted.")
        except Exception as e:
            messagebox.showerror("Error", "An unexpected error occurred: " + str(e))


class MessageSignaturePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Back Button
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(DSSApp))
        back_button.grid(row=0, column=0, pady=10, padx=10, sticky="nw")

        # Sign Message Button
        sign_message_button = tk.Button(self, text="Sign a Message",
                                        command=lambda: self.controller.show_frame(SignMessagePage))
        sign_message_button.grid(row=1, column=1, padx=100, pady=10)

        # Verify Signature Button
        verify_signature_button = tk.Button(self, text="Verify Message Signature",
                                            command=lambda: self.controller.show_frame(MessageVerifyPage))
        verify_signature_button.grid(row=2, column=1, padx=100, pady=10)


class FileSignaturePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Back Button
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(DSSApp))
        back_button.grid(row=0, column=0, pady=10, padx=10, sticky="nw")

        # Sign File Button
        sign_file_button = tk.Button(self, text="Sign a File", command=lambda: self.controller.show_frame(SignFilePage))
        sign_file_button.grid(row=1, column=1, padx=120, pady=10)

        # Verify File Signature Button
        verify_file_signature_button = tk.Button(self, text="Verify File Signature",
                                                 command=lambda: self.controller.show_frame(FileVerifyPage))
        verify_file_signature_button.grid(row=2, column=1, padx=120, pady=10)


class DSSApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Кнопка повернення
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(MainAppPage))
        back_button.grid(row=0, column=1, pady=10, padx=10, sticky="nw")

        # Кнопка для генерації пари ключів
        generate_keys_button = tk.Button(self, text="Generate Key Pair", command=self.generate_key_pair)
        generate_keys_button.grid(row=4, column=3, padx=(115, 0), pady=10)

        encrypt_button = tk.Button(self, text="Message signature",
                                   command=lambda: self.controller.show_frame(MessageSignaturePage))
        encrypt_button.grid(row=2, column=3, padx=(120, 0), pady=10)

        # Кнопка для дешифрування файлу
        decrypt_button = tk.Button(self, text="File signature",
                                   command=lambda: self.controller.show_frame(FileSignaturePage))
        decrypt_button.grid(row=3, column=3, padx=(120, 0), pady=10)

    @staticmethod
    def generate_key_pair():
        size = 1024
        key = DSA.generate(bits=size)
        private_key = key.exportKey()
        public_key = key.publickey().exportKey()

        # Запитуємо імена файлів у користувача
        private_key_filename = simpledialog.askstring("Save Private Key", "Enter a name for the private key file:")
        public_key_filename = simpledialog.askstring("Save Public Key", "Enter a name for the public key file:")

        flag1 = False
        # Збереження приватного ключа
        if private_key_filename:
            private_key_path = filedialog.asksaveasfilename(
                initialfile=private_key_filename,
                defaultextension=".pem",
                filetypes=[("PEM files", "*.pem")],
                title="Save Private Key"
            )
            if private_key_path:
                flag1 = True

        flag2 = False
        # Збереження публічного ключа
        if public_key_filename:
            public_key_path = filedialog.asksaveasfilename(
                initialfile=public_key_filename,
                defaultextension=".pem",
                filetypes=[("PEM files", "*.pem")],
                title="Save Public Key"
            )
            if public_key_path:
                flag2 = True

        # Перевірка, чи користувач вказав шляхи
        if all((flag1, flag2)):
            # Збереження приватного ключа
            with open(private_key_path, "wb") as pr_file:
                pr_file.write(private_key)

                # Збереження публічного ключа
            with open(public_key_path, "wb") as pub_file:
                pub_file.write(public_key)

            messagebox.showinfo("Success", "Key pair generated and saved successfully.")
        else:
            messagebox.showerror("Error", "Key pair generation cancelled or incomplete.")

