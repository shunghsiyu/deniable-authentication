from __future__ import division, print_function
import timeit

from deniable.original import Original
from Crypto import Random
import os

__author__ = 'shunghsiyu'

A = 'Alice'

def benchmark(input_size, count):
    setup = """
import random
import string
import os
from deniable.original import Original
from Crypto.PublicKey import RSA
from Crypto import Random

A = '{}'
obj = Original(A)
data = Random.get_random_bytes({})
cipher_text = obj.enc(data, A, A)
cipher_text_b64 = obj.enc_base64(data, A, A)
""".format(A, input_size)
    stmt_enc = "obj.enc(data, A, A)"
    stmt_enc_b64 = "obj.enc_base64(data, A, A)"
    stmt_dec = "obj.dec(cipher_text)"
    stmt_dec_b64 = "obj.dec_base64(cipher_text_b64)"

    # BINARY
    t1 = timeit.Timer(stmt=stmt_enc, setup=setup)
    print('Test Original ENCRYPTION to BINARY with {} bytes and running {} times'.format(input_size, count))
    print(t1.timeit(count) / count)
    t2 = timeit.Timer(stmt=stmt_dec, setup=setup)
    print('Test Original DECRYPTION to BINARY with {} bytes and running {} times'.format(input_size, count))
    print(t2.timeit(count) / count)
    output_size = get_output_size(input_size)
    print('The input size is {} and the BINARY output size is {}'.format(input_size, output_size))
    print('The ratio is {}'.format(output_size/input_size))
    print()

    # BASE64
    t3 = timeit.Timer(stmt=stmt_enc_b64, setup=setup)
    print('Test Original ENCRYPTION to BASE64 with {} bytes and running {} times'.format(input_size, count))
    print(t3.timeit(count) / count)
    t4 = timeit.Timer(stmt=stmt_dec_b64, setup=setup)
    print('Test Original DECRYPTION to BASE64 with {} bytes and running {} times'.format(input_size, count))
    print(t4.timeit(count) / count)
    output_size_b64 = get_output_size(input_size, encoding='base64')
    print('The input size is {} and the BASE64 output size is {}'.format(input_size, output_size))
    print('The ratio is {}'.format(output_size_b64/input_size))

    print('-----')

def get_output_size(input_size, encoding='binary'):
    data = Random.get_random_bytes(input_size)
    if encoding.lower() in ['base64', 'b64']:
        cipher_text = Original(A).enc_base64(data, A, A)
    else:
        cipher_text = Original(A).enc(data, A, A)
    return len(cipher_text)

if __name__ == '__main__':
    os.chdir('keys/rsa/')
    run = 3
    benchmark(100*2**10, 500*run)
    benchmark(1*2**20, 100*run)
    benchmark(10*2**20, 10*run)
    benchmark(100*2**20, 1*run)
