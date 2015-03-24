from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Cipher.PKCS1_OAEP import PKCS1OAEP_Cipher
from Crypto.Hash import HMAC, SHA256
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import _RSAobj
from Crypto.Signature import PKCS1_PSS
from Crypto.Signature.PKCS1_PSS import PSS_SigScheme
from Crypto.Util import Counter
from payload import Payload, Container

__author__ = 'shunghsiyu'

class Original:
    def __init__(self):
        print('init')

    def enc(self, data, A, B):
        n = 32
        iv = 1L
        ctr = Counter.new(128, initial_value=iv)

        priA = self.privatekey(A)
        assert isinstance(priA, _RSAobj)
        pubB = self.publickey(B)
        assert isinstance(pubB, _RSAobj)
        signer = PKCS1_PSS.new(priA)
        assert isinstance(signer, PSS_SigScheme)
        rsa = PKCS1_OAEP.new(pubB, SHA256)
        assert isinstance(rsa, PKCS1OAEP_Cipher)

        k = Random.get_random_bytes(n)

        aesk = AES.new(k, AES.MODE_CTR, ctr)
        D = aesk.encrypt(data)

        hmac = HMAC.new(k, D, SHA256)
        M = hmac.digest()

        ABk = Container(A, B, k).serialize()
        hashABk = SHA256.new(ABk).digest()
        S = signer.sign(hashABk)

        ABkS = Container(A, B, k, S).serialize()
        H = rsa.encrypt(ABkS)
        return Payload(H, D, M).serialize()

    def dec(self, payload):
        print('dec')
        raise NotImplementedError()

    def publickey(self, target):
        raise NotImplementedError()
        return None

    def privatekey(self, target):
        raise NotImplementedError()
        return None

raise NotImplementedError()