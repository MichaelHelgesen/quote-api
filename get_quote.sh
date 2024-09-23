#!/bin/bash
read -p "Name: " NAME
curl http://127.0.0.1:5000/person/$NAME/quote | jq .
