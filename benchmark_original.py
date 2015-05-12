import timeit
import sys
__author__ = 'shunghsiyu'

count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
size = int(sys.argv[1])

setup = """
import random
import string
import os
from original import Original
from Crypto.PublicKey import RSA
from Crypto import Random

A = ''.join(random.choice(string.ascii_letters) for _ in range(12))
rsaA = RSA.generate(2048)
with open(A, 'w') as f:
    f.write(rsaA.exportKey('PEM'))
with open(A+'.pub', 'w') as f:
    f.write(rsaA.publickey().exportKey('PEM'))
obj = Original(A)
data = Random.get_random_bytes({})
cipher_text = obj.enc(data, A, A)
""".format(size)
stmt_enc = "obj.enc(data, A, A)"
stmt_dec = "obj.dec(cipher_text)"

t1 = timeit.Timer(stmt=stmt_enc, setup=setup)
print('Test Original ENCRYPTION with {} bytes and running {} times'.format(size, count))
print(t1.timeit(count)/count)

t2 = timeit.Timer(stmt=stmt_enc, setup=setup)
print('Test Original DECRYPTION with {} bytes and running {} times'.format(size, count))
print(t2.timeit(count)/count)

print('-----')