#!/bin/bash
read -p "Name of person: " NAME 
echo $NAME

curl -X POST \
    -d '{"name":"'${NAME}'" }' \
    -H 'Content-Type: application/json' \
    http://127.0.0.1:5000/person


