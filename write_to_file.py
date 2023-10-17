import datetime
from tkinter import messagebox


class WriteToFile:
    @staticmethod
    def write_to_file(**kwargs):
        """
        Записує числа в файл "random_numbers.txt" і, якщо переданий параметр 'period', записує також період генерації.

        :param numbers: Список чисел для запису в файл.
        :param period: (необов'язковий) Період функції генерації.
        """
        if 'numbers' in kwargs.keys():
            with open("random_numbers" + str(datetime.datetime.now().strftime("%H:%M:%S")).replace(":", "-")
                      + "--" + str(datetime.datetime.now().strftime("%d:%m:%Y")).replace(":", "-") + ".txt",
                      "w", encoding="utf-8") as file:
                if 'period' in kwargs.keys():
                    file.write(f"Період функції генерації: {kwargs['period']}")
                    file.write("\n")
                for i, el in enumerate(kwargs['numbers']):
                    if not i % 20 and i != 0:
                        file.write("\n")
                    file.write(str(el) + " ")
                file.write("\n")

    @staticmethod
    def save_hash_to_file(md5_hash, filename):
        ex = ".txt"
        with open(str(filename) + ".txt", "w") as hash_file:
            hash_file.write(md5_hash)
            messagebox.showinfo("Success", f"MD5 hash saved to '{filename + ex}'")
