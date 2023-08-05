from pathlib import Path
import os
from Crypto.PublicKey import RSA
import base64


def generate_key_pair(passphrase_private,
                      passphrase_public,
                      root_path=""):
    """
    :param passphrase_private:  String
    :param passphrase_public: String
    :param root_path:  String
    :return:
    """
    new_key = RSA.generate(4096, e=65537)
    print(f"key_original: {new_key}")
    private_key = new_key.exportKey(
        format='PEM',
        passphrase=passphrase_private,
        pkcs=8,
        protection="scryptAndAES128-CBC")

    public_key = new_key.publickey().exportKey(
        format='PEM',
        passphrase=passphrase_public,
        pkcs=8,
        protection="scryptAndAES128-CBC")

    path_private = os.path.join(root_path, "private.pem")
    print(f"path_private: {path_private}")
    path_public = os.path.join(root_path, "public.pem")
    print(f"path_private: {path_public}")

    private_key_path = Path(path_private)
    private_key_path.touch(mode=0o600)
    private_key_path.write_bytes(private_key)

    public_key_path = Path(path_public)
    public_key_path.touch(mode=0o664)
    public_key_path.write_bytes(public_key)


def generate_b64encode(key):
    """
    :param key: String Bytes
    """
    if not isinstance(key, bytes):
        raise Exception('require key in bytes')

    unencoded = bytes(f'{key}', "utf-8")
    encoded = base64.b64encode(unencoded)
    return encoded


def generate_b64decode(key):
    """
    :param key: String Bytes
    """
    decoded = base64.b64decode(key)
    return decoded
