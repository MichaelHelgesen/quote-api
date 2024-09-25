#!/bin/bash
read -p "QUOTE ID: " QUOTE_ID
read -p "Tag name: " TAG_NAME
curl -X POST \
    -d '{"name": "'${TAG_NAME}'"}' \
    -H 'Content-Type: application/json' \
    http://127.0.0.1:5000/quote/$QUOTE_ID/tag


