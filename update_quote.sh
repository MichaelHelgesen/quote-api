#!/bin/bash
read -p "ID: " ID
read -p "QUOTE: " QUOTE
read -p "SOURCE: " SOURCE
curl -X PUT \
    -d '{"quote": "'${QUOTE}'", "source": "'${SOURCE}'"}' \
    -H 'Content-Type: application/json' \
    http://127.0.0.1:5000/quote/$ID
