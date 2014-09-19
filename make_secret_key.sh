#!/bin/bash

# Generates a Flask secret_key in the file 'secret_key'
# Reference: http://flask.pocoo.org/snippets/104/

uuidgen | tr -d - > secret_key
echo Secret key stored in file: secret_key