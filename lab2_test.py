import unittest
from md5 import MD5Hash
import hashlib


class TestMD5Hash(unittest.TestCase):

    def setUp(self):
        self.md5_hasher = MD5Hash()

    def test_md5_known_values(self):
        # Test with known values
        self.assertEqual(self.md5_hasher.md5(bytearray("abc", "utf-8")), "900150983cd24fb0d6963f7d28e17f72")
        self.assertEqual(self.md5_hasher.md5(bytearray("", "utf-8")), "d41d8cd98f00b204e9800998ecf8427e")

    def test_md5_empty_string(self):
        self.assertEqual(self.md5_hasher.md5(bytearray("", "utf-8")), "d41d8cd98f00b204e9800998ecf8427e")

    def test_md5_long_string(self):
        long_string = "a" * 1000  # A very long string
        self.assertEqual(self.md5_hasher.md5(bytearray(long_string, "utf-8")),
                         str(hashlib.md5(long_string.encode()).hexdigest()))

    def test_md5_non_ascii_characters(self):
        self.assertEqual(self.md5_hasher.md5(bytearray("测试", "utf-8")), str(hashlib.md5("测试".encode()).hexdigest()))


if __name__ == '__main__':
    unittest.main()
