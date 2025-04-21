#!/bin/bash
cd zd
./make.bash
cd ..

cd util
./make.bash
cd ..

node zd/das2json.mjs part.drawio
python3 main.py . - '' main part.drawio.json | node util/decodeoutput.mjs
