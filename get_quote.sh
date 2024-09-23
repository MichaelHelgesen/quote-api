#!/bin/bash
read -p "ID: " ID
curl http://127.0.0.1:5000/quote/$ID | jq .
