#!/bin/bash

# Script to make a local copy certain bits of t2t/
# only if the BOOTSTRAPPT environment variable is set

# Check if BOOTSTRAPPT environment variable is set
if [ -n "${BOOTSTRAPPT}" ]; then
    # Check if the source file exists
    if [ -d ~/projects/t2t ]; then
        cp ~/projects/t2t/nanodsl .
	chmod a+x nanodsl
	cp -R ~/projects/t2t/lib .
        echo "t2t has been copied"
    else
        echo "Error: ~/projects/t2t/ does not exist."
        exit 1
    fi
else
    exit 0
fi
