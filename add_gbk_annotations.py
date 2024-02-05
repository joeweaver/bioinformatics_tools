from Bio import SeqIO
from argparse import ArgumentParser
import pandas as pd

def parse_args():
    parser = ArgumentParser(description="Given a GBK file and file of annotations, add annotations. Annotations file is a csv file where each annotation is one line with five columns: seq, by, match, key, value." )
    parser.add_argument("-i", "--input", type=str, required=True, help="Input GBK file (required)")
    parser.add_argument("-a", "--annotation_file", type=str, required=True, help="File with annotations.")
    parser.add_argument("-n", "--nomatch", nargs="*", type=str, required=False, help="Key-value pairs of defaults if no match.")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file (required)")
    return parser.parse_args()

def annotate_gbk(gbk,annotations,defaults=None):
    def_records=[]
    for gbk_record in gbk:
        features = []
        if defaults:
            for feat in gbk_record.features:
                for k, v in defaults.items():
                    feat.qualifiers[k] = v
                features.append(feat)
            gbk_record.features = features
        def_records.append(gbk_record)

    records=[]
    for gbk_record in def_records:
        for note in annotations.iterrows():
            if note[1][0] == gbk_record.name:
                features = []
                for feat in gbk_record.features:
                    if feat.qualifiers[note[1][1]][0] == note[1][2]:
                        feat.qualifiers[note[1][3]] = [note[1][4]]
                    features.append(feat)
                gbk_record.features= features
        records.append(gbk_record)
    return records


def main():
    args = parse_args

if __name__ == "__main__":
    args = parse_args()
    gbk = SeqIO.parse(args.input, "genbank")
    annotations = pd.read_csv(args.annotation_file,header=None)
    defaults=None
    if args.nomatch:
        defaults = dict(zip(args.nomatch[::2], args.nomatch[1::2]))
    annotated = annotate_gbk(gbk, annotations, defaults)
    SeqIO.write(annotated,args.output,"genbank")