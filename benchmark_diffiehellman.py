import timeit
import sys
__author__ = 'shunghsiyu'

count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
size = int(sys.argv[1])

setup = """
import random
import string
import os
from diffiehellman import DiffieHellman
from test_diffiehellman import export_key
from Crypto.Random import random
from Crypto.PublicKey import ElGamal
from Crypto.PublicKey.ElGamal import ElGamalobj
from Crypto import Random

A = ''.join(random.choice(string.ascii_letters) for _ in range(12))
keyA = ElGamal.generate(2048, Random.new().read)
with open(A, 'w') as f:
    f.write(export_key(keyA))
with open(A+'.pub', 'w') as f:
    f.write(export_key(keyA.publickey()))
obj = DiffieHellman(A)
data = Random.get_random_bytes({})
cipher_text = obj.enc(data, A, A)
""".format(size)
stmt_enc = "obj.enc(data, A, A)"
stmt_dec = "obj.dec(cipher_text)"

t1 = timeit.Timer(stmt=stmt_enc, setup=setup)
print('Test DiffieHellman ENCRYPTION with {} bytes and running {} times'.format(size, count))
print(t1.timeit(count)/count)

t2 = timeit.Timer(stmt=stmt_dec, setup=setup)
print('Test DiffieHellman DECRYPTION with {} bytes and running {} times'.format(size, count))
print(t2.timeit(count)/count)

print('-----')