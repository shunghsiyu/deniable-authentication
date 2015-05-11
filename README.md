# deniable-authentication

## Requirements

* PyCrypto
* PyXB (only for code generation)

### Setting up Virutalenv

This step is not necessary but may help avoid python package conflicts.

1. In the shell `mkdir virtualenv; virtualenv --python=python2.7 ./virtualenv`
2. Then `source ./virtualenv/bin/activate`

## Instructions

### Installing Requirements

1. `pip install pycrypto pyxb`

### Generating XML Generator

1. To generate python source file from XML Schema files use command
    * `pyxbgen -u original_container.xsd -m gen/original_containerxml`
    * `pyxbgen -u original_payload.xsd -m gen/original_payloadxml`
    * `pyxbgen -u diffiehellman_container.xsd -m gen/diffiehellman_containerxml`
    * `pyxbgen -u diffiehellman_payload.xsd -m gen/diffiehellman_payloadxml`
