#!/bin/bash
read -p "ID QUOTE: " QUOTE_ID
read -p "ID TAG: " TAG_ID
curl -X DELETE \
    http://127.0.0.1:5000/quote/$QUOTE_ID/tag/$TAG_ID | jq .
