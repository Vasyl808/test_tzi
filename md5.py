import math


class MD5Hash:
    def __init__(self):
        self.__ABCD = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
        self.__T = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]
        self.__shift_values = [[7, 12, 17, 22],
                             [5, 9, 14, 20],
                             [4, 11, 16, 23],
                             [6, 10, 15, 21]]
        self.__funcs = [self.__F, self.__G, self.__H, self.__I]

    def __F(self, x, y, z):
        return (x & y) | (~x & z)

    def __G(self, x, y, z):
        return (x & z) | (y & ~z)

    def __H(self, x, y, z):
        return x ^ y ^ z

    def __I(self, x, y, z):
        return y ^ (x | ~z)

    def __shift(self, x, amount):
        x %= 2 ** 32
        return ((x << amount) | (x >> (32 - amount))) % 2 ** 32

    def __index_to_reshuffle(self, x):
        if x < 16:
            return x
        if 16 <= x < 32:
            return (1 + 5 * x) % 16
        if 32 <= x < 48:
            return (5 + 3 * x) % 16
        if 48 <= x < 64:
            return (7 * x) % 16

    def md5(self, message: bytearray) -> str:
        orig_len_in_bits = (8 * len(message)) % 2 ** 32
        message.append(128)

        while len(message) % 64 != 56:
            message.append(0)
        message += orig_len_in_bits.to_bytes(8, byteorder='little')

        registers = self.__ABCD[:]

        for chunk_length in range(0, len(message), 64):
            a, b, c, d = registers
            chunk = message[chunk_length:chunk_length + 64]

            for i in range(64):
                f = self.__funcs[i // 16](b, c, d)
                ind = self.__index_to_reshuffle(i)
                bb = (b + self.__shift(a + f + self.__T[i] + int.from_bytes(chunk[4 * ind:4 * ind + 4], byteorder='little'),
                                  self.__shift_values[i // 16][i % 4])) & 0xFFFFFFFF
                a, b, c, d = d, bb, b, c

            for i, val in enumerate([a, b, c, d]):
                registers[i] = (registers[i] + val) & 0xFFFFFFFF

        return '{:032x}'.format(int.from_bytes(sum(x << (32 * i) for i, x in
                                            enumerate(registers)).to_bytes(16, byteorder='little'),byteorder='big'))

