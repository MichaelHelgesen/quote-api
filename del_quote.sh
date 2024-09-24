#!/bin/bash
read -p "ID: " ID
curl -X DELETE \
    http://127.0.0.1:5000/quote/$ID | jq .
