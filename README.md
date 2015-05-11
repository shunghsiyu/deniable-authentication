# deniable-authentication

## Requirements

* PyCrypto
* PyXB

### Setting up Virutalenv

1. In the shell type `mkdir virtualenv; virtualenv --python=python2.7 ./virtualenv`
2. Then type `source ./virtualenv/bin/activate`
3. Then `pip install pycrypto pyxb`
4. Then generate python source file from XML Schema files
    * `pyxbgen -u original_container.xsd -m gen/original_containerxml`
    * `pyxbgen -u original_payload.xsd -m gen/original_payloadxml`
    * `pyxbgen -u diffiehellman_container.xsd -m gen/diffiehellman_containerxml`
    * `pyxbgen -u diffiehellman_payload.xsd -m gen/diffiehellman_payloadxml`
