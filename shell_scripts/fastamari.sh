#!/usr/bin/env bash

set -euo pipefail

output_file="combined.tar.gz"
verbose=false

print_help() {
    cat <<EOF
This is a very alpha version meant to be a quick script to help combine individually tarred fastq files into one.  It may act oddly if not applied in that scenario - e.g. it can and will try to cat the contents of any single-file containing tar.gz it processes

Usage: $(basename "$0") [-o output_name] [-h] [file1.tar.gz file2.tar.gz ...]

Concatenate contents from all .tar.giz files, or those matching the optional pattern,  in the current directory.

EACH ARCHIVE SHOULD CONTAIN EXACTLY ONE FILE

Options:
 -o FILENAME  Set the output filename (default: combined.tar.gz)
 -v           Show version
 -V	          Verbose mode
 -h           Show this help message
 
Arguments:
 file1.tar.gz file2.tar.gz ...   Optional list of archive files or globs to process.
                                 If omitted, defaults to all *.tar.gz in current directory.

Examples:
  $(basename "$0")                       # Process all .tar.gz in current directory
  $(basename "$0") *.tar.gz              # Process all matching files from glob
  $(basename "$0") -o output.tar.gz a.tar.gz b.tar.gz  # Process specified files with custom output filename
EOF
}

shift $((OPTIND - 1))

# If no files are provided as args, default to *.tar.gz
if [[ $# -eq 0 ]]; then
    FILES=( *.tar.gz )
else
    FILES=( "$@" )
fi

if [[ ${#FILES[@]} -eq 1 && "${FILES[0]}" == '*.tar.gz' ]]; then
    echo "Error: No .tar.gz files found in the current directory." >&2
    exit 1
fi

# parse args
while getopts ":o:hvV" opt; do
    case $opt in
        o)
            output_file="$OPTARG"
            ;;
        h)
            print_help
            exit 0
            ;;
        v)
            echo "version 0.0.1"
            exit 0
            ;;
        V)
            verbose=true
            ;;
        \?)
            echo "Unknown option: -$OPTARG" >&2
            print_help
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            print_help
            exit 1
            ;;
    esac
done

for f in "${FILES[@]}"; do
    if [[ ! -f "$f" ]]; then
        echo "Warning: '$f' is not a regular file, skipping." >&2
        continue
    fi
    
    if $verbose; then
        echo "Processing $f..."
    fi
    file_count=$(tar -tzf "$f" | wc -l)

	if [[ "$file_count" -ne 1 ]]; then
	    echo "Error: Archive '$f' contains $file_count files (expected exactly 1)" >&2
	    exit 1
	fi
    tar -xOzf "$f" >> "combined.fastq"
done

tar -czf "$output_file" "combined.fastq"
rm "combined.fastq"

if $verbose; then
    echo "Wrote combined contents to $output_file"
fi
