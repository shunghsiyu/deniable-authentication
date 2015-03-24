from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import _RSAobj
from Crypto.Signature import PKCS1_PSS
from Crypto.Signature.PKCS1_PSS import PSS_SigScheme
from Crypto.Util import Counter
from payload import Payload

__author__ = 'shunghsiyu'

class Original:
    def __init__(self):
        print('init')

    def enc(self, data, A, B):
        assert isinstance(A, _RSAobj)
        assert isinstance(B, _RSAobj)
        n = 32
        ctr = Counter.new(128, initial_value=1L)

        k = Random.get_random_bytes(n)
        aes = AES.new(k, AES.MODE_CTR, ctr)
        hmac = HMAC.new(k, SHA256)
        sha256 = SHA256.new()
        signer = PKCS1_PSS.new(A)
        D = aes.encrypt(data)
        M = hmac.digest()
        assert isinstance(signer, PSS_SigScheme)
        hashABk = SHA256.new(A + B + k).digest()
        S = signer.sign(hashABk)
        H = ''
        raise NotImplementedError()
        return Payload(H, D, M)

    def dec(self, payload):
        print('dec')

raise NotImplementedError()