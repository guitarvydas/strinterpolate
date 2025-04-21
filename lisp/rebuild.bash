#!/bin/bash
node das2json.mjs part.drawio
python3 main.py . - '' main part.drawio.json | node decodeoutput.mjs
