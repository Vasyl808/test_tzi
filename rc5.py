import os
from generator import NumberGenerator
from md5 import MD5Hash
import time


class RC5:
    def __init__(self, key, w=64, R=16, b=32):
        self.w = w
        self.R = R
        self.key = key
        self.T = 2 * (R + 1)
        self.block_size = w // 4
        self.word_bytes = w // 8
        self.mod = 2 ** self.w
        self.b = b

        self.setL()
        self.setS()
        self.shuffle()

    @staticmethod
    def get_md5_key(password) -> bytearray:
        return bytearray(MD5Hash().md5(bytearray(password.encode())), encoding='utf-8')

    def shift_L(self, a: int, s: int) -> int:
        s %= self.w
        number = (a << s) | (a >> self.w - s)
        number %= 2 ** self.w
        return number

    def shift_R(self, a: int, s: int) -> int:
        s %= self.w
        number = (a >> s) | (a << self.w - s)
        number %= 2 ** self.w
        return number

    def setL(self):
        if self.b == 0:
            self.c = 1
        elif self.b % self.word_bytes:
            self.key += b'\x00' * (self.word_bytes - self.b % self.word_bytes)
            self.b = len(self.key)
            self.c = self.b // self.word_bytes
        else:
            self.c = self.b // self.word_bytes
        L = [0] * self.c
        for i in range(self.b - 1, -1, -1):
            L[i // self.word_bytes] = (L[i // self.word_bytes] << 8) + self.key[i]
        self.L = L

    def getP(self):
        if self.w == 16:
            return 0xB7E1
        elif self.w == 32:
            return 0xB7E15163
        elif self.w == 64:
            return 0xB7E151628AED2A6B

    def getQ(self):
        if self.w == 16:
            return 0x9E37
        elif self.w == 32:
            return 0x9E3779B9
        elif self.w == 64:
            return 0x9E3779B97F4A7C15

    def setS(self):
        P = self.getP()
        Q = self.getQ()

        self.S = [P + Q * i for i in range(self.T)]

    def shuffle(self):
        i, j, A, B = 0, 0, 0, 0
        for k in range(max(self.c, self.T)):
            A = self.S[i] = self.shift_L((self.S[i] + A + B), 3)
            B = self.L[j] = self.shift_L((self.L[j] + A + B), A + B)
            i = (i + 1) % len(self.S)
            j = (j + 1) % len(self.L)

    def init_vector(self):
        x0 = int(time.time()) % (2 ** 8)
        result = bytearray()
        generator = NumberGenerator.from_config_file("config.json", x0, self.block_size)
        numbers = generator.generate()
        for _ in range(self.block_size):
            x0 = numbers[_] % (2 ** 8)
            result.append(x0)
        return result

    def encode_block(self, data):
        A = (data >> self.w) % self.mod
        B = data % self.mod
        A = (A + self.S[0]) % self.mod
        B = (B + self.S[1]) % self.mod
        for i in range(1, self.R + 1):
            A = (self.shift_L((A ^ B), B) + self.S[2 * i]) % self.mod
            B = (self.shift_L((A ^ B), A) + self.S[2 * i + 1]) % self.mod
        return ((A << self.w) | B).to_bytes(length=self.block_size, byteorder='little')

    def encode_file(self, input_filename, output_filename):
        with open(input_filename, 'rb') as inp, open(output_filename, 'wb') as out:
            start_time = time.time()
            run = True
            init_vector = self.init_vector()
            out.write(init_vector)
            encoded_text = init_vector
            while run:
                text = inp.read(self.block_size)
                if not text:
                    break
                if len(text) != self.block_size:
                    text = bytearray(text)
                    append_value = self.block_size - len(text)
                    for _ in range(append_value):
                        text.append(append_value)
                    run = False
                text_int = int.from_bytes(text, byteorder='little')
                encoded_text_int = int.from_bytes(encoded_text, byteorder='little')
                text_int ^= encoded_text_int
                encoded_text = self.encode_block(text_int)
                out.write(encoded_text)
        end_time = time.time()
        return f"File encrypted in {end_time - start_time:.5f} seconds."

    def decode_block(self, data):
        A = data >> self.w
        B = data % self.mod
        for i in range(self.R, 0, -1):
            B = self.shift_R((B - self.S[2 * i + 1]) % self.mod, A) ^ A
            A = self.shift_R((A - self.S[2 * i]) % self.mod, B) ^ B
        B = (B - self.S[1]) % self.mod
        A = (A - self.S[0]) % self.mod
        return (A << self.w) | B

    def decode_file(self, input_filename, output_filename):
        with open(input_filename, 'rb') as inp, open(output_filename, 'wb+') as out:
            start_time = time.time()
            init_vector = inp.read(self.block_size)
            prev_encoded_text = init_vector
            run = True
            while run:
                encoded_text = inp.read(self.block_size)
                if not encoded_text:
                    break
                if len(encoded_text) != self.block_size:
                    run = False
                encoded_text_int = int.from_bytes(encoded_text, byteorder='little')
                text_int = self.decode_block(encoded_text_int) ^ int.from_bytes(prev_encoded_text, byteorder='little')
                text = text_int.to_bytes(length=self.block_size, byteorder='little')
                prev_encoded_text = encoded_text
                #last_byte = text[-1]
                #if last_byte <= len(text):
                #    for byte in text[-last_byte:]:
                #        if byte != last_byte:
                #            break
                #    else:
                #        text = text[:-last_byte]
                out.write(text)
        end_time = time.time()
        return f"File decrypted in {end_time - start_time:.5f} seconds."

#if __name__ == '__main__':
#    key = input('Enter key: ')
#    rc5 = RC5(RC5.get_md5_key(key), 64, 16)
#    action = input('Choose action:\n1 - encode\n2 - decode\nYour choice: ')
#    filename = input('Enter filename: ')

#    if action == '1':
#        rc5.encode_file(filename, os.path.join('encoded_' + filename))
#        print('Done!')
#    elif action == '2':
#        rc5.decode_file(filename, os.path.join('decoded_' + filename))
#        print('Done!')
#    else:
#        print('The action doesn`t exists.')
#        #encoded_document (6).pdf