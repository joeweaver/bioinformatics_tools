from Bio import SeqIO
from argparse import ArgumentParser

# TODO test against more complicated features, coordinates
# TODO multiple 'by' criteria?
def parse_args():
    parser = ArgumentParser(description="Filter a GBK file based on matches to a feature qualifier. Will retain all seq between the matches, but no CDs not explicitly matching the filter. WIP works for simple features/qualifiers and coordinates." )
    parser.add_argument("-i", "--input", type=str, required=True, help="Input GBK file (required)")
    parser.add_argument("-b", "--by", type=str, required=True, help="Identifier for feature (required)")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file (required)")
    parser.add_argument("-k", "--keep", nargs="*", type=str, required=True, help="List of Values to retain (required)")
    return parser.parse_args()

def filter_gbk(gbk,filter_by,keep,output):
    gbk_records = SeqIO.parse(gbk, "genbank")
    records = []
    for gbk_record in gbk_records:
        retained_feats = []
        for feat in gbk_record.features:
            if feat.qualifiers[filter_by][0] in keep:
                retained_feats.append(feat)
        if(retained_feats):
            trimmed_gbk_record = gbk_record
            trimmed_gbk_record.features = retained_feats
            feats_begin=min([int(f.location.start) for f in trimmed_gbk_record.features])
            feats_end=max([int(f.location.end) for f in trimmed_gbk_record.features])
            trimmed_gbk_record = trimmed_gbk_record[feats_begin:feats_end]
            records.append(trimmed_gbk_record)
    SeqIO.write(records, output, "genbank")

if __name__ == "__main__":
    args = parse_args()
    filter_gbk(args.input, args.by, args.keep, args.output)
