import tkinter as tk


class MainAppPage(tk.Frame):
    def __init__(self, parent, controller):
        from md5_app import HashApp
        from number_generator_app import NumberGeneratorApp
        from rc5_app import RC5App
        from rsa_app import RSAApp
        from dss_app import DSSApp
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Main Page")
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Pseudorandom number generator",
                            command=lambda: controller.show_frame(NumberGeneratorApp))
        button2 = tk.Button(self, text="M5 hash",
                            command=lambda: controller.show_frame(HashApp))
        button3 = tk.Button(self, text="RC5 encryption",
                            command=lambda: controller.show_frame(RC5App))
        button4 = tk.Button(self, text="RSA encryption",
                            command=lambda: controller.show_frame(RSAApp))
        button5 = tk.Button(self, text="Digital signature",
                            command=lambda: controller.show_frame(DSSApp))
        button1.pack(pady=5)
        button3.pack(pady=5)
        button4.pack(pady=5)
        button5.pack(pady=5)
        button2.pack(pady=5)
