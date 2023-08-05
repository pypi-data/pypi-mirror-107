import base64
import zlib

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


class CryptoFiles(object):

    def encrypt(self, encrypt_file, public_key, passphrase_public):
        """
        :params encrypt_file: file_path
        :params public_key: Object
        :params passphrase_public: String
        Returns: String
        """

        rsa_key = RSA.importKey(extern_key=public_key.read_bytes(), passphrase=passphrase_public)
        rsa_key = PKCS1_OAEP.new(rsa_key)

        encrypt_file = zlib.compress(encrypt_file.read_bytes())

        chunk_size = 470
        offset = 0
        end_loop = False
        encrypted = bytearray()

        while not end_loop:
            chunk = encrypt_file[offset:offset + chunk_size]
            if len(chunk) % chunk_size != 0:
                end_loop = True
                chunk += bytes(chunk_size - len(chunk))
            encrypted += rsa_key.encrypt(chunk)
            offset += chunk_size
        return base64.b64encode(encrypted)

    def decrypt(self, encrypted_file, private_key, passphrase_private):
        """
        :params encrypted_file: encoded file
        :params private_key: Object
        :params passphrase_private: String
        Returns: String
        """

        rsakey = RSA.importKey(extern_key=private_key.read_bytes(), passphrase=passphrase_private)
        rsakey = PKCS1_OAEP.new(rsakey)

        encrypted_file = base64.b64decode(encrypted_file)

        chunk_size = 512
        offset = 0
        decrypted = bytearray()

        while offset < len(encrypted_file):
            chunk = encrypted_file[offset: offset + chunk_size]
            decrypted += rsakey.decrypt(chunk)
            offset += chunk_size
        return zlib.decompress(decrypted)
