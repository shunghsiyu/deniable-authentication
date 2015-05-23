---
title: Read Me
---

# Requirements

* PyCrypto

## Installing Requirements

`pip install pycrypto`

# Usage

## Weakly Deniable Scheme

### Generate Key

Generate a public/private RSA key pair for the Weakly Deniable scheme.

 * `main_weak gen $KEY_SIZE`
     - `KEY_SIZE` (*required*) is the key size of the key pair in bits
     - Asks the name of the user associated with the key through `stdin`

### Encryption

Encrypt the content of the file with the Weakly Deniable scheme.

 * `main_weak enc $RECIPIENT $INPUT`
     - `INPUT` (*required*) is the path to the file which its content will be encrypted
     - Assume the user's name is stored in file `./identity`, the uesr's name is used to find the private key of the current user that will be used for encryption
     - Output the result to `stdout`
 * `main_weak enc $RECIPIENT $INPUT $OUTPUT --identity $IDENTITY_FILE`
     - `INPUT` (*required*) is the path to the file which its content will be encrypted
     - `OUTPUT` (*optional*) is the path to the file where the result will be stored
     - `IDENTITY_FILE` (*optional*) instead of using `./default` use the file in this path to find the name of the user

### Decryption

Decrypt the content of the file encrypted by the Weakly Deniable scheme.

 * `main_weak dec $INPUT`
     - `INPUT` (*required*) is the path to the file which its content will be decrypted
     - Assume the user's name is stored in file `./identity`, the uesr's name is used to find the private key of the current user that will be used for decryption
     - Output the result to `stdout`
 * `main_weak dec $INPUT $OUTPUT --identity $IDENTITY_FILE`
     - `INPUT` (*required*) is the path to the file which its content will be decrypted
     - `OUTPUT` (*optional*) is the path to the file where the result will be stored
     - `IDENTITY_FILE` (*optional*) instead of using `./default` use the file in this path to find the name of the user

### Example

The following works in BASH

 1. Generate a key pair
    - `main_weak gen 1024`
 2. Name the user `alice`
    - `Please enter your preferred username: alice` (Enter)
 3. Move the identity file so it will not be overwritten
    - `mv identity identity1`
 4. Generate another key pair
    - `main_weak gen 1024`
 5. Name the user `bob`
    - `Please enter your preferred username: bob` (Enter)
 6. Create a message to encrypt
    - `echo 'A Message' > message.txt`
 7. Encrypt a message for alice as bob
    - `main_weak enc alice message.txt message.txt.enc`
 8. Decrypt the message from bob as alice
    - `main_weak dec message.txt.enc --identity identity1`
    - 'A Message' is printed in shell

## Strongly Deniable Scheme

### Generate Key

Generate a public/private ElGamal key pair for the Strongly Deniable scheme. The key generation is different from the Weakly Deniable scheme because the **sender and recipient MUST have the same key parameter $p$ and $g$**.

 * `main_strong gen $KEY_SIZE`
     - `KEY_SIZE` (*required*) is the key size of the key pair in bits
     - Asks the name of the user associated with the key through `stdin`
 * `main_strong gen --parameter_from ANOTHER_KEY`
     - `ANOTHER_KEY` the path to the file which stores an ElGamal key, the key parameters in the file will be used to generate the new key
     - Asks the name of the user associated with the key through `stdin`

### Encryption

Encrypt the content of the file with the Strongly Deniable scheme.

 * `main_strong enc $RECIPIENT $INPUT`
     - `INPUT` (*required*) is the path to the file which its content will be encrypted
     - Assume the user's name is stored in file `./identity`, the uesr's name is used to find the private key of the current user that will be used for encryption
     - Output the result to `stdout`
 * `main_strong enc $RECIPIENT $INPUT $OUTPUT --identity $IDENTITY_FILE`
     - `INPUT` (*required*) is the path to the file which its content will be encrypted
     - `OUTPUT` (*optional*) is the path to the file where the result will be stored
     - `IDENTITY_FILE` (*optional*) instead of using `./default` use the file in this path to find the name of the user

### Decryption

Decrypt the content of the file encrypted by the Strongly Deniable scheme.

 * `main_strong dec $INPUT`
     - `INPUT` (*required*) is the path to the file which its content will be decrypted
     - Assume the user's name is stored in file `./identity`, the uesr's name is used to find the private key of the current user that will be used for decryption
     - Output the result to `stdout`
 * `main_strong dec $INPUT $OUTPUT --identity $IDENTITY_FILE`
     - `INPUT` (*required*) is the path to the file which its content will be decrypted
     - `OUTPUT` (*optional*) is the path to the file where the result will be stored
     - `IDENTITY_FILE` (*optional*) instead of using `./default` use the file in this path to find the name of the user

### Example

The following works in BASH

 1. Generate a key pair
    - `main_strong gen 1024`
 2. Name the user `alice`
    - `Please enter your preferred username: alice` (Enter)
 3. Move the identity file so it will not be overwritten
    - `mv identity identity1`
 4. Generate another key pair
    - `main_strong gen --parameter_from alice.pub`
 5. Name the user `bob`
    - `Please enter your preferred username: bob` (Enter)
 6. Create a message to encrypt
    - `echo 'A Message' > message.txt`
 7. Encrypt a message for alice as bob
    - `main_strong enc alice message.txt message.txt.enc`
 8. Decrypt the message from bob as alice
    - `main_strong dec message.txt.enc --identity identity1`
    - 'A Message' is printed in shell

# License

The MIT License (MIT)

Copyright (c) 2015 Paolo Gasti, Kasper Bonne Rasmussen, Shung-Hsi Yu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
