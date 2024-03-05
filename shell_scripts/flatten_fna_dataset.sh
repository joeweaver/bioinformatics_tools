#!/usr/bin/env bash

set -euo pipefail

# In a directory containing an unzipped  NCBI dataset download of fna 
# files, flatten it by copying them all up to the execution directory
# and rename them to simpler GCA/F_accession.fna.

# Also copy the dataset_catlog.json and assembly_data_report.jsonl to the flattened directory

# NB. Does not update paths in dataset_catalog as there's been no 
# personal need to do so yet.

# NB. Does not check for collisons between accession numbers, as
# the datasets I've been pulling so far all have unique accnos.

# Does not automatically rm or trash the original files or locations

find . -name 'GC[FA]_*.fna' -exec cp {} . \;
rename 's|(GC[AF]_\d+\.\d+).*\.fna|$1.fna|' *.fna

find . -name 'assembly_data_report.jsonl' -exec cp {} . \;
find . -name 'dataset_catalog.json' -exec cp {} . \;
