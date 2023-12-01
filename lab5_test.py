import unittest
from unittest import mock
from unittest.mock import Mock, patch, MagicMock, mock_open
from tkinter import Tk
from dss_app import DSSApp, SignMessagePage, MessageVerifyPage, SignFilePage, FileVerifyPage
import tkinter as tk


class TestDSSApp(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app = DSSApp(parent=self.root, controller=Mock())

    def test_generate_key_pair(self):
        # Mock dialogs and message boxes
        with patch('tkinter.filedialog.asksaveasfilename', return_value='testfile.pem') as mock_savefile,\
             patch('tkinter.simpledialog.askstring', return_value='test') as mock_askstring,\
             patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.generate_key_pair()

            # Verify file dialog and message box interactions
            mock_savefile.assert_called()
            mock_askstring.assert_called()
            mock_showinfo.assert_called_with("Success", "Key pair generated and saved successfully.")


class TestSignMessagePage(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = SignMessagePage(self.root, None)

    @patch("tkinter.filedialog.askopenfilename", return_value="")
    def test_load_private_key_cancel(self, mock_askopenfilename):
        self.app.load_private_key()
        self.assertEqual(self.app.private_key_label.cget("text"), "No file selected")

    def tearDown(self):
        self.root.destroy()


class TestSignFilePage(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = SignFilePage(self.root, None)

    @patch("os.path.getsize", return_value=1024)
    @patch("tkinter.filedialog.askopenfilename", return_value="path/to/file")
    def test_load_file_valid(self, mock_askopenfilename, mock_getsize):
        self.app.load_file()
        self.assertEqual(self.app.file_path_label.cget("text"), "path/to/file")

    @patch("tkinter.filedialog.askopenfilename", return_value="")
    def test_load_file_cancel(self, mock_askopenfilename):
        self.app.load_file()
        self.assertEqual(self.app.file_path_label.cget("text"), "No file selected for signing")


class TestMessageVerifyPage(unittest.TestCase):
    @patch('tkinter.Toplevel')
    def setUp(self, mock_toplevel):
        # Замінюємо Toplevel, щоб вікно не відкривалось
        self.root = tk.Tk()
        self.root.withdraw()  # Ховаємо головне вікно
        self.app = MessageVerifyPage(self.root, None)

    @patch("tkinter.filedialog.askopenfilename", return_value="")
    def test_load_public_key_cancel(self, mock_askopenfilename):
        self.app.load_public_key()
        self.assertEqual(self.app.public_key_label.cget("text"), "No public key loaded")

    @patch("tkinter.messagebox.showerror")
    @patch("tkinter.messagebox.showinfo")
    @patch("Cryptodome.Signature.DSS.new")
    @patch("Cryptodome.Hash.SHA256.new")
    def test_verify_signature_valid(self, mock_hash_new, mock_dss_new, mock_showinfo, mock_showerror):
        self.app.public_key = MagicMock()
        self.app.signature_entry.insert(tk.END, "valid_signature")
        self.app.string_text.insert(tk.END, "test message")

        self.app.verify_signature()

        mock_hash_new.assert_called_once()
        mock_dss_new.assert_called_once()


class TestFileVerifyPage(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = FileVerifyPage(self.root, None)

    @patch("builtins.open", new_callable=mock_open, read_data="signature_data")
    @patch("tkinter.filedialog.askopenfilename", return_value="path/to/signature")
    @patch("os.path.getsize", return_value=1024)  # Додаємо підміну для os.path.getsize
    def test_load_signature_file_valid(self, mock_askopenfilename, mock_file_open, mock_getsize):
        self.app.load_signature_file()
        self.assertEqual(self.app.signature_entry.get("1.0", tk.END).strip(), "signature_data")

    @patch("tkinter.filedialog.askopenfilename", return_value="")
    def test_load_signature_file_cancel(self, mock_askopenfilename):
        self.app.load_signature_file()
        self.assertEqual(self.app.signature_entry.get("1.0", tk.END).strip(), "")


if __name__ == '__main__':
    unittest.main()
