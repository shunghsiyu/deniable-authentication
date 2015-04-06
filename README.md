# deniable-authentication

## Requirements

* PyCrypto
* PyXB

### Setting up Virutalenv

1. In the shell type `mkdir virtualenv; virtualenv2.7 --python=python2.7 ./virtualenv`
2. Then type `source ./virtualenv/bin/activate`
3. Then `pip2.7 install pycrypto pyxb`
4. Then generate python source file from XML Schema files
    * Type `pyxb -u payload.xml -m gen/payloadxml`
    * and `pyxb -u container.xml -m gen/containerxml`
