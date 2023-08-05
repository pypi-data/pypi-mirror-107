import base64
import hashlib
import logging
import binascii
from Crypto.Cipher import AES

logger = logging.getLogger(__name__)


def md5(s: str, salt='', encoding='utf-8') -> str:
    return hashlib.md5((s + salt).encode(encoding=encoding)).hexdigest()


def base64Encode(s) -> bytes:
    s = str(s)
    return base64.b64encode(s.encode('utf-8'))


def base64Decode(s) -> str:
    s = str(s)
    return base64.b64decode(s).decode('utf-8')


def hex_to_bytes(s: str):
    return binascii.a2b_hex(s)


class CryptoModel:
    """
    AES加密类
    """

    def __init__(self, key, iv, mode=AES.MODE_CBC):
        self.key = md5(key).encode()
        self.iv = md5(iv).encode()[8:24]
        self.mode = mode

    @staticmethod
    def padding(text):
        padding_0a = (16 - len(text) % 16) * b' '
        return text.encode('utf-8') + padding_0a

    def aes_encode(self, text):
        obj = AES.new(self.key, self.mode, self.iv)
        data = self.padding(text)
        return obj.encrypt(data)

    def aes_decode(self, data):
        obj = AES.new(self.key, self.mode, self.iv)
        return obj.decrypt(data)

    def encrypt(self, data):
        ' 加密函数 '
        cryptor = AES.new(self.key, self.mode, self.iv)
        return binascii.b2a_hex(cryptor.encrypt(data)).decode()

    def decrypt(self, data):
        ' 解密函数 '
        cryptor = AES.new(self.key, self.mode, self.iv)
        return cryptor.decrypt(binascii.a2b_hex(data)).decode()
