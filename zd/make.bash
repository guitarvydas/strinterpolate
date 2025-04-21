#!/bin/bash

# Script to copy kernel0d.py from ~/projects/rt to the current directory, and das2json.js
# only if the BOOTSTRAPPT environment variable is set

# Check if BOOTSTRAPPT environment variable is set
if [ -n "${BOOTSTRAPPT}" ]; then
    # Check if the source file exists
    if [ -f ~/projects/rt/out.py ]; then
        # Copy the file to the current directory
        cp ~/projects/rt/out.py ./kernel0d.py
        echo "kernel0d.py has been copied to the current directory."
    else
        echo "Error: ~/projects/rt/out.py does not exist."
        exit 1
    fi
    if [ -f ~/projects/rt/stubbed-out-repl.py ]; then
        # Copy the file to the current directory
        cp ~/projects/rt/stubbed-out-repl.py ./repl.py
        echo "stubbed-out-repl.py has been copied to the current directory as repl.py."
    else
        echo "Error: ~/projects/rt/stubbed-out-repl.py does not exist."
        exit 1
    fi
    if [ -f ~/projects/0D/das2json/das2json.mjs ]; then
        # Copy the file to the current directory
        cp ~/projects/0D/das2json/das2json.mjs .
        echo "das2json.js has been copied to the current directory."
    else
        echo "Error: ~/projects/0D/das2json/das2json.mjs does not exist."
        exit 1
    fi
else
    exit 0
fi
