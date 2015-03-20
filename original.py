from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import RSA
from Crypto.Util import Counter

__author__ = 'shunghsiyu'

class Original:
    def __init__(self):
        print('init')

    def enc(self, data, A, B):
        n = 32
        ctr = Counter.new(128, initial_value=1L)

        k = Random.get_random_bytes(n)
        aes = AES.new(k, AES.MODE_CTR, ctr)
        D = aes.encrypt(data)
        M = HMAC.new(k, SHA256).digest()
        S = ''
        H = ''
        raise NotImplementedError()
        return H + D + M

    def dec(self, payload):
        print('dec')

raise NotImplementedError()