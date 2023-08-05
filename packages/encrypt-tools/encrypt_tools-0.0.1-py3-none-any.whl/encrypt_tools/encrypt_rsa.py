import os
from base64 import b64decode
from base64 import b64encode

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


class CrypyoRsa(object):
    def encrypt(self, data, passphrase_public, root_path=""):
        """
        :params data: String
        :params passphrase_public: String
        :params root_path: default: ""
        Returns: String
        """
        path_public = os.path.join(root_path, "public.pem")

        plaintext = b64encode(data.encode())
        encoded_key = open(path_public, "rb").read()
        key = RSA.import_key(extern_key=encoded_key, passphrase=passphrase_public)

        rsa_encryption_cipher = PKCS1_OAEP.new(key)
        ciphertext = rsa_encryption_cipher.encrypt(plaintext)
        return b64encode(ciphertext).decode()

    def decrypt(self, encrypted_data, passphrase_private, root_path=""):
        """
        :params encrypted_data: String
        :params passphrase_private: String
        :params root_path: default: ""
        Returns: String
        """
        path_private = os.path.join(root_path, "private.pem")

        encoded_key = open(path_private, "rb").read()
        key = RSA.import_key(extern_key=encoded_key, passphrase=passphrase_private)

        ciphertext = b64decode(encrypted_data.encode())
        rsa_decryption_cipher = PKCS1_OAEP.new(key)
        plaintext = rsa_decryption_cipher.decrypt(ciphertext)
        return b64decode(plaintext).decode()
