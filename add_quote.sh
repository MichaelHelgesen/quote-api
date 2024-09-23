#!/bin/bash
read -p "PERSON ID: " PERSON_ID
read -p "Quote: " QUOTE
read -p "Source: " SOURCE
curl -X POST \
    -d '{"quote": "'${QUOTE}'", "source": "'${SOURCE}'", "person_id": "'${PERSON_ID}'"}' \
    -H 'Content-Type: application/json' \
    http://127.0.0.1:5000/quote


