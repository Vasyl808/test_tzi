import unittest
import os
import tempfile
from Cryptodome.PublicKey import RSA
from rsa import RSAImplement


class TestRSAImplement(unittest.TestCase):

    @staticmethod
    def generate_rsa_key_pair(key_size=1024):
        key = RSA.generate(key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

    def setUp(self):
        self.private_key, self.public_key = self.generate_rsa_key_pair()

        # Write the keys to temporary files
        self.private_key_file = tempfile.NamedTemporaryFile(delete=False)
        self.private_key_file.write(self.private_key)
        self.private_key_file.close()

        self.public_key_file = tempfile.NamedTemporaryFile(delete=False)
        self.public_key_file.write(self.public_key)
        self.public_key_file.close()

    def test_encryption_decryption(self):
        original_content = b"Hello, World!"

        # Create a temporary file with some content
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(original_content)
            temp_filename = temp.name

        encrypted_filename = temp_filename + ".enc"
        decrypted_filename = temp_filename + ".dec"

        # Test encryption
        RSAImplement.perform_encryption(encrypted_filename, self.public_key_file.name, temp_filename)

        # Test decryption
        RSAImplement.perform_decryption(decrypted_filename, self.private_key_file.name, encrypted_filename)

        # Verify that the decrypted content matches the original
        with open(decrypted_filename, 'rb') as f:
            decrypted_content = f.read()

        self.assertEqual(original_content, decrypted_content)

        # Clean up temporary files
        os.remove(temp_filename)
        os.remove(encrypted_filename)
        os.remove(decrypted_filename)

    # Additional test cases can be added here for different scenarios

    def tearDown(self):
        # Delete the temporary key files
        os.remove(self.private_key_file.name)
        os.remove(self.public_key_file.name)


if __name__ == '__main__':
    unittest.main()
