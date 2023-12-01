import tkinter as tk

from main_page import MainAppPage
from md5_app import HashApp, StringHashPage, FileHashPage, VerifyIntegrityPage
from number_generator_app import NumberGeneratorApp
from rc5_app import RC5App, EncodePage, DecodePage
from rsa_app import RSAApp, EncryptionPage, DecryptionPage
from dss_app import DSSApp, FileSignaturePage, MessageSignaturePage, SignMessagePage, SignFilePage, MessageVerifyPage,\
    FileVerifyPage


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("App")
        self.geometry("450x400")
        self.resizable(False, False)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainAppPage, NumberGeneratorApp, HashApp, StringHashPage, FileHashPage, VerifyIntegrityPage,
                  RC5App, EncodePage, DecodePage, RSAApp, EncryptionPage, DecryptionPage, DSSApp, FileSignaturePage,
                  MessageSignaturePage, SignMessagePage, SignFilePage, FileVerifyPage, MessageVerifyPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainAppPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
