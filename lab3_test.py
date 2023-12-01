import unittest
import os
import tempfile
from rc5 import RC5


class TestRC5(unittest.TestCase):

    def setUp(self):
        self.key = "secret_key"
        self.rc5 = RC5(RC5.get_md5_key(self.key))

    def test_encode_decode_block(self):
        original_data = 1234567890  # some integer data
        encoded_data = self.rc5.encode_block(original_data)
        decoded_data = self.rc5.decode_block(int.from_bytes(encoded_data, byteorder='little'))
        self.assertEqual(original_data, decoded_data)

    def test_file_encryption_decryption(self):
        original_content = b""

        # Create a temporary file with some content
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(original_content)
            temp_filename = temp.name

        encrypted_filename = temp_filename + ".enc"
        decrypted_filename = temp_filename + ".dec"

        # Test file encryption
        self.rc5.encode_file(temp_filename, encrypted_filename)

        # Test file decryption
        self.rc5.decode_file(encrypted_filename, decrypted_filename)

        # Verify that the decrypted content matches the original
        with open(decrypted_filename, 'rb') as f:
            decrypted_content = f.read()

        self.assertEqual(original_content, decrypted_content)

        # Clean up temporary files
        os.remove(temp_filename)
        os.remove(encrypted_filename)
        os.remove(decrypted_filename)


if __name__ == '__main__':
    unittest.main()
