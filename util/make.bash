#!/bin/bash

# Script to copy utility files from ~/projects/util
# only if the BOOTSTRAPPT environment variable is set

# Check if BOOTSTRAPPT environment variable is set
if [ -n "${BOOTSTRAPPT}" ]; then
    # Check if the source file exists
    if [ -d ~/projects/util/ ]; then
        # Copy the file to the current directory
        cp ~/projects/util/* .
        echo "utilities have been copied"
    else
        echo "Error: ~/projects/util/ does not exist."
        exit 1
    fi
else
    exit 0
fi
