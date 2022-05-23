#!/bin/bash

in="$1"

if [ ! -d memeAnnotations ]; then
	mkdir -p memeAnnotations
fi

python meme-annotate.py --motifs ${in} > memeAnnotations/${in}.gff