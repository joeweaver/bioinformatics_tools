#!/usr/bin/env bash

set -euo pipefail

# Given a fasta file list output a column of all the accession numbers
# assumes an NCBI style fasta where the accno is the first word after the >

if [ $# -ne 1 ]; then
    echo "Need to specify a fasta file: $0 <filename>"
    exit 1
fi

fasta_file=$1

seqkit seq -n "$fasta_file" | awk '{print $1}'
