#!/bin/bash
read -p "NAME: " NAME
read -p "Quote: " QUOTE
read -p "Source: " SOURCE
curl -X POST \
    -d '{"quote": "'${QUOTE}'", "source": "'${SOURCE}'"}' \
    -H 'Content-Type: application/json' \
    http://127.0.0.1:5000/person/$NAME/quote


