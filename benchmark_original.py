from __future__ import division
from original import Original
from Crypto import Random
import timeit
import os
__author__ = 'shunghsiyu'

A = 'Alice'

def benchmark(input_size, count):
    setup = """
import random
import string
import os
from original import Original
from Crypto.PublicKey import RSA
from Crypto import Random

A = '{}'
obj = Original(A)
data = Random.get_random_bytes({})
cipher_text = obj.enc(data, A, A)
""".format(A, input_size)
    stmt_enc = "obj.enc(data, A, A)"
    stmt_dec = "obj.dec(cipher_text)"
    t1 = timeit.Timer(stmt=stmt_enc, setup=setup)
    print('Test Original ENCRYPTION with {} bytes and running {} times'.format(input_size, count))
    print(t1.timeit(count) / count)
    output_size = get_output_size(input_size)
    print('The input size is {} and the output size is {}'.format(input_size, output_size))
    print('The ratio is {}'.format(output_size/input_size))
    t2 = timeit.Timer(stmt=stmt_dec, setup=setup)
    print('Test Original DECRYPTION with {} bytes and running {} times'.format(input_size, count))
    print(t2.timeit(count) / count)
    print('-----')

def get_output_size(input_size):
    data = Random.get_random_bytes(input_size)
    cipher_text = Original(A).enc(data, A, A)
    return len(cipher_text)

if __name__ == '__main__':
    os.chdir('keys/rsa/')
    run = 3
    benchmark(100*2**10, 500*run)
    benchmark(1*2**20, 100*run)
    benchmark(10*2**20, 10*run)
    benchmark(100*2**20, 1*run)
