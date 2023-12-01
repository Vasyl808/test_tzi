from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, AES
import time

from Cryptodome.Random import get_random_bytes


class RSAImplement:
    @staticmethod
    def perform_encryption(rsa_pub_filename, filename):
        # Генерація випадкового ключа AES
        aes_key = get_random_bytes(16)  # AES ключ розміром 128 біт

        # Шифрування файлу за допомогою AES
        cipher_aes = AES.new(aes_key, AES.MODE_EAX)
        with open(filename, "rb") as file:
            ciphertext, tag = cipher_aes.encrypt_and_digest(file.read())

        # Шифрування ключа AES за допомогою RSA
        with open(rsa_pub_filename, "rb") as rsa_file:
            rsa_public = PKCS1_OAEP.new(RSA.importKey(rsa_file.read()))
            encrypted_aes_key = rsa_public.encrypt(aes_key)

        # Збереження зашифрованого AES ключа та зашифрованих даних
        with open('encrypted_' + filename, 'wb') as out_file:
            for x in [encrypted_aes_key, cipher_aes.nonce, tag, ciphertext]:
                out_file.write(x)

    @staticmethod
    def perform_decryption(rsa_pr_filename, filename):
        with open(rsa_pr_filename, "rb") as rsa_file:
            rsa_private = PKCS1_OAEP.new(RSA.importKey(rsa_file.read()))

        with open(filename, "rb") as file:
            encrypted_aes_key, nonce, tag, ciphertext = \
                [file.read(x) for x in (128, 16, 16, -1)]  # 128 байт для RSA ключа, 16 для nonce і tag

            # Розшифрування AES ключа
            aes_key = rsa_private.decrypt(encrypted_aes_key)

            # Розшифрування файлу
            cipher_aes = AES.new(aes_key, AES.MODE_EAX, nonce)
            data = cipher_aes.decrypt_and_verify(ciphertext, tag)

        with open('decrypted_' + filename, 'wb') as out_file:
            out_file.write(data)


print('Menu:\n1. Get key pair\n2. Encrypt file\n3. Decrypt file')

selection = int(input('Your selection: '))

if selection == 1:
    size = 1024
    key = RSA.generate(bits=size)

    with open("private.pem", "wb") as pr_file:
        pr_file.write(key.exportKey())
    with open("public.pem", "wb") as pub_file:
        pub_file.write(key.publickey().exportKey())
    print('Success.')
elif selection == 2:
    rsa_pub_filename = input('RSA public key file: ')
    filename = input('Filename: ')
    start_time = time.time()
    RSAImplement.perform_encryption(rsa_pub_filename, filename)
    print('Success. Time:' + str(time.time() - start_time))
elif selection == 3:
    rsa_pr_filename = input('RSA private key file: ')
    filename = input('Filename: ')
    start_time = time.time()
    RSAImplement.perform_decryption(rsa_pr_filename, filename)
    print('Success. Time: ' + str(time.time() - start_time))


#Success. Time: 0.02264115333557129
#Success. Time: 0.05264115333557129