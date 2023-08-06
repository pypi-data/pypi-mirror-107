import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

key = b"teamuniphi@cunninghamroadfrmbang"
bs = AES.block_size

class AESCipher(object):

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw.encode())

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]