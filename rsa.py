import time

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP


class RSAImplement:
    @staticmethod
    def perform_encryption(encrypted_filename, public_key_path, file_to_encrypt_path):
        with open(public_key_path, "rb") as rsa_file:
            rsa_public = PKCS1_OAEP.new(RSA.importKey(rsa_file.read()))

        max_block_size = 32  # для ключа 1024 біт
        start_time = time.time()
        with open(file_to_encrypt_path, "rb") as file, open(encrypted_filename, 'wb') as out_file:
            while True:
                block = file.read(max_block_size)
                if not block:
                    break
                encrypted_block = rsa_public.encrypt(block)
                out_file.write(encrypted_block)
        end_time = time.time()
        return f"File encrypted in {end_time - start_time:.5f} seconds."

    @staticmethod
    def perform_decryption(decrypted_filename, private_key_path, file_to_decrypt_path):

        with open(private_key_path, "rb") as rsa_file:
            rsa_private = PKCS1_OAEP.new(RSA.importKey(rsa_file.read()))
        max_block_size = 128  # Для 1024-бітного ключа RSA

        start_time = time.time()
        with open(file_to_decrypt_path, "rb") as file, open(decrypted_filename, 'wb') as out_file:
            while True:
                block = file.read(max_block_size)
                if not block:
                    break
                decrypted_block = rsa_private.decrypt(block)
                out_file.write(decrypted_block)
        end_time = time.time()
        return f"File decrypted in {end_time - start_time:.5f} seconds."
