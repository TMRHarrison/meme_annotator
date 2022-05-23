#!/bin/bash

in="$1"

if [ ! -d mastAnnotations ]; then
	mkdir -p mastAnnotations
fi

python mast-annotate.py --mast ${in} > mastAnnotations/${in}.gff