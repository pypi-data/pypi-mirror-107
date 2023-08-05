from base64 import b64encode, b64decode

from Crypto.Cipher import AES


class CryptoAes(object):

    def encrypt(self, data, key, iv):
        """
        :params data: String
        :params key: String Bytes
        :params iv: String Bytes
        Returns: String
        """
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return b64encode(cipher.encrypt(self.__pad(data).encode())).decode()

    def decrypt(self, encrypted_data, key, iv):
        """
        :params encrypted_data: String
        :params key: String Bytes
        :params iv: String Bytes
        Returns: String
        """
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return self.__unpad(cipher.decrypt(b64decode(encrypted_data)).decode())

    def __pad(self, text):
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]
