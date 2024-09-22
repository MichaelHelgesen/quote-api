#!/bin/bash

curl -X POST \
    -d '{"name": "monet"}' \
    -H 'Content-Type: application/json' \
    http://127.0.0.1:5000/person


