#!/usr/bin/env bash

set -euo pipefail

# Given a TSV file and a file with 'interesting' strings,
# output only the rows from the TSV file where the specified column matches the string

# n.b. used GPT here to recall some specifics of how bash and awk worked

# assume 3 args, if not 3 args, print a reminder
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <file_to_scan.tsv> <strings_file> <column_name>"
    exit 1
fi

# assign args to better named vars
file_to_scan="$1"
strings_file="$2"
column_name="$3"

# check if files exist
if [ ! -f "$file_to_scan" ]; then
    echo "Error: File '$file_to_scan' not found!"
    exit 1
fi

if [ ! -f "$strings_file" ]; then
    echo "Error: File '$strings_file' not found!"
    exit 1
fi

# actually perform the filtering
awk -v col="$column_name" -F'\t' 'BEGIN { OFS = FS } NR == 1 || FNR == NR { strings[$0] = 1; next } { for (string in strings) { if ($col ~ string) { print; break } } }' "$strings_file" "$file_to_scan"
