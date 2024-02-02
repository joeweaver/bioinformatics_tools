from Bio import SeqIO
from BCBio import GFF
from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser(description="Combine an NCBI fna and prodigal gff into a GBK with sequence data")
    parser.add_argument("-f", "--fasta", type=str, required=True, help="Input FNA file (required)")
    parser.add_argument("-g", "--gff", type=str, required=True, help="Input gff file (required)")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output file (required)")
    return parser.parse_args()


def merge(fna, gff, outfile):
    """Given a fna from NCBI datasets and prodigal generated gff from the same fna,
    merge into a well-formatted GBK which includes sequence data and all CDs
    heavily borrowed from Brad Chapman https://github.com/chapmanb/bcbb/blob/master/gff/Scripts/gff/gff_to_genbank.pyS
    """
    fasta_input = SeqIO.to_dict(SeqIO.parse(fna, "fasta"))
    gff_iter = GFF.parse(gff, fasta_input)
    SeqIO.write(_check_gff(_fix_ncbi_id(gff_iter), "DNA"), outfile, "genbank")


def _fix_ncbi_id(fasta_iter):
    """GenBank identifiers can only be 16 characters; try to shorten NCBI.
    """
    for rec in fasta_iter:
        if len(rec.name) > 16 and rec.name.find("|") > 0:
            new_id = [x for x in rec.name.split("|") if x][-1]
            print("Warning: shortening NCBI name %s to %s" % (rec.id, new_id))
            rec.id = new_id
            rec.name = new_id
        yield rec


def _check_gff(gff_iterator, molecule_type):
    """Check GFF files before feeding to SeqIO to be sure they have sequences.
    """
    for rec in gff_iterator:
        if "molecule_type" not in rec.annotations:
            rec.annotations["molecule_type"] = molecule_type
        yield _flatten_features(rec)


def _flatten_features(rec):
    """Make sub_features in an input rec flat for output.

    GenBank does not handle nested features, so we want to make
    everything top level.
    """
    out = []
    for f in rec.features:
        cur = [f]
        while len(cur) > 0:
            nextf = []
            for curf in cur:
                out.append(curf)
                if len(curf.sub_features) > 0:
                    nextf.extend(curf.sub_features)
            cur = nextf
    rec.features = out
    return rec


if __name__ == "__main__":
    args = parse_args()
    merge(args.fasta, args.gff, args.output)
