from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
import time
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog

from loading_window import LoadingWindowRSA
from main_page import MainAppPage
from rsa import RSAImplement
import os


class EncryptionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Кнопка повернення
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(RSAApp))
        back_button.grid(row=0, column=0, pady=10, padx=10, sticky="nw")

        # Відцентроване розміщення елементів
        self.grid_columnconfigure(0, weight=1)

        # Кнопка для вибору публічного ключа
        select_key_button = tk.Button(self, text="Select Public Key", command=self.select_public_key)
        select_key_button.grid(row=1, column=0, pady=10)

        # Відображення шляху до публічного ключа
        self.key_path_label = tk.Label(self, text="No public key selected")
        self.key_path_label.grid(row=2, column=0, pady=10)

        # Кнопка для вибору файлу для шифрування
        select_file_button = tk.Button(self, text="Select File to Encrypt", command=self.select_file_to_encrypt)
        select_file_button.grid(row=3, column=0, pady=10)

        # Відображення шляху до файлу для шифрування
        self.file_path_label = tk.Label(self, text="No file selected")
        self.file_path_label.grid(row=4, column=0, pady=10)

        # Кнопка для шифрування файлу
        encrypt_button = tk.Button(self, text="Encrypt File", command=self.encrypt_file)
        encrypt_button.grid(row=5, column=0, pady=10)

        self.public_key_path = None
        self.file_to_encrypt_path = None

    def select_public_key(self):
        self.public_key_path = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
        self.key_path_label.config(
            text=f"Selected key: {self.public_key_path}" if self.public_key_path else "No public key selected")

    def select_file_to_encrypt(self):
        self.file_to_encrypt_path = filedialog.askopenfilename()
        self.file_path_label.config(
            text=f"Selected file: {self.file_to_encrypt_path}" if self.file_to_encrypt_path else "No file selected")

    def encrypt_file(self):
        if not self.public_key_path or not self.file_to_encrypt_path:
            messagebox.showerror("Error", "Please select a public key and a file to encrypt.")
            return

        if os.path.getsize(self.file_to_encrypt_path) > 1028 * 1028:
            messagebox.showerror("Error", "File size exceeds 1 MB.")
            return
        file_extension = os.path.splitext(self.file_to_encrypt_path)[1]
        encrypted_filename = filedialog.asksaveasfilename(defaultextension=f"{file_extension}",
                                                          filetypes=[(file_extension, f"*{file_extension}")])
        if encrypted_filename:
            loading_window = LoadingWindowRSA(self, RSAImplement.perform_encryption, "Encrypting...",
                                              encrypted_filename, self.public_key_path, self.file_to_encrypt_path)
            loading_window.wait_window()


class DecryptionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Кнопка повернення
        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(RSAApp))
        back_button.grid(row=0, column=0, pady=10, padx=10, sticky="nw")

        # Відцентроване розміщення елементів
        self.grid_columnconfigure(0, weight=1)

        # Кнопка для вибору приватного ключа
        select_key_button = tk.Button(self, text="Select Private Key", command=self.select_private_key)
        select_key_button.grid(row=1, column=0, pady=10)

        # Відображення шляху до приватного ключа
        self.key_path_label = tk.Label(self, text="No private key selected")
        self.key_path_label.grid(row=2, column=0, pady=10)

        # Кнопка для вибору файлу для дешифрування
        select_file_button = tk.Button(self, text="Select File to Decrypt", command=self.select_file_to_decrypt)
        select_file_button.grid(row=3, column=0, pady=10)

        # Відображення шляху до файлу для дешифрування
        self.file_path_label = tk.Label(self, text="No file selected")
        self.file_path_label.grid(row=4, column=0, pady=10)

        # Кнопка для дешифрування файлу
        decrypt_button = tk.Button(self, text="Decrypt File", command=self.decrypt_file)
        decrypt_button.grid(row=5, column=0, pady=10)

        self.private_key_path = None
        self.file_to_decrypt_path = None

    def select_private_key(self):
        self.private_key_path = filedialog.askopenfilename(filetypes=[("PEM files", "*.pem")])
        self.key_path_label.config(
            text=f"Selected key: {self.private_key_path}" if self.private_key_path else "No private key selected")

    def select_file_to_decrypt(self):
        self.file_to_decrypt_path = filedialog.askopenfilename()
        self.file_path_label.config(
            text=f"Selected file: {self.file_to_decrypt_path}" if self.file_to_decrypt_path else "No file selected")

    def decrypt_file(self):
        if not self.private_key_path or not self.file_to_decrypt_path:
            messagebox.showerror("Error", "Please select a private key and a file to decrypt.")
            return

        if os.path.getsize(self.file_to_decrypt_path) > 1028 * 1028 * 4:
            messagebox.showerror("Error", "File size exceeds 4 MB.")
            return

        file_extension = os.path.splitext(self.file_to_decrypt_path)[1]
        decrypted_filename = filedialog.asksaveasfilename(defaultextension=f"{file_extension}",
                                                          filetypes=[(file_extension, f"*{file_extension}")])
        if decrypted_filename:
            loading_window = LoadingWindowRSA(self, RSAImplement.perform_decryption, "Decrypting...",
                                              decrypted_filename, self.private_key_path, self.file_to_decrypt_path)
            loading_window.wait_window()


class RSAApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Кнопка повернення
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(MainAppPage))
        back_button.grid(row=0, column=1, pady=10, padx=10, sticky="nw")

        # Кнопка для генерації пари ключів
        generate_keys_button = tk.Button(self, text="Generate Key Pair", command=self.generate_key_pair)
        generate_keys_button.grid(row=4, column=3, padx=(114, 0), pady=10)

        # Кнопка для шифрування файлу
        encrypt_button = tk.Button(self, text="Encrypt File", command=lambda: self.controller.show_frame(EncryptionPage))
        encrypt_button.grid(row=2, column=3, padx=(120, 0), pady=10)

        # Кнопка для дешифрування файлу
        decrypt_button = tk.Button(self, text="Decrypt File", command=lambda: self.controller.show_frame(DecryptionPage))
        decrypt_button.grid(row=3, column=3, padx=(120, 0), pady=10)

    @staticmethod
    def generate_key_pair():
        size = 1024
        key = RSA.generate(bits=size)
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


# Success. Time:0.021003246307373047
# Success. Time: 0.027008771896362305
