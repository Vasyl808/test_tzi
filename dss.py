from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import DSA
from Cryptodome.Signature import DSS

if __name__ == '__main__':
    print("1 - Generate keys")
    print("2 - Sign message")
    print("3 - Verify message")
    k = int(input("Choose: "))
    if k == 1:
        pub = input('Public key file: ')
        priv = input('Private key file: ')

        key = DSA.generate(bits=1024)
        with open(priv, "wb") as input_file_pr:
            input_file_pr.write(key.exportKey())
        with open(pub, "wb") as input_file_pb:
            input_file_pb.write(key.publickey().exportKey())

    elif k == 2:
        private_file = input('Private key file: ')
        with open(private_file, 'rb') as file:
            private_key = DSA.import_key(file.read())
        print('1 - From file')
        print('2 - From console')
        m = int(input("Choose: "))
        message = ''
        if m == 1:
            filename = input('Filename: ')
            with open(filename, 'rb') as file:
                message = file.read()
        elif m == 2:
            message = bytes(input('Message: '), encoding='utf-8')

        mess_enc = SHA256.new(message)
        sign = DSS.new(private_key, 'fips-186-3')
        signature = sign.sign(mess_enc)

        print('Signed message: ' + signature.hex())
        write_to_file = input('Write to file? (y/n)')

        if write_to_file == 'y':
            filename = input('Filename: ')
            with open(filename, 'w') as output:
                output.write(signature.hex())
    elif k == 3:
        public_file = input('Public key file: ')
        with open(public_file, 'rb') as file:
            public_key = DSA.import_key(file.read())
        message = str.encode(input('Message: '))
        print('1 - From file')
        print('2 - From console')
        m = int(input("Choose: "))
        signature = ''
        if m == 1:
            filename = input('Filename: ')
            with open(filename, 'r') as file:
                signature = file.read()
        elif m == 2:
            signature = input('Signature: ')

        message = SHA256.new(message)
        signature = bytes.fromhex(signature)
        verifier = DSS.new(public_key, 'fips-186-3')

        try:
            verifier.verify(message, signature)
            print("Valid signature")
        except ValueError:
            print("Invalid signature")
        pass
