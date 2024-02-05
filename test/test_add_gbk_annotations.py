import add_gbk_annotations
from Bio import SeqIO
from filecmp import cmp
import pandas as pd

def test_annotate_gbk_with_defaults():
    gbk = SeqIO.parse("data/test_multirecord_assembly.gbk", "genbank")
    anns = pd.read_csv("data/test_annofile.csv", header=None)
    defs = {"short_name": " ", "long_name": "NoMatch"}
    to_write = add_gbk_annotations.annotate_gbk(gbk,anns,defs)
    SeqIO.write(to_write, "output/annotated_gbk_defaults.gbk", "genbank")
    assert cmp("output/annotated_gbk_defaults.gbk","expected/annotated_gbk_defaults.gbk")

def test_annotate_gbk_with_no_defaults():
    gbk = SeqIO.parse("data/test_multirecord_assembly.gbk", "genbank")
    anns = pd.read_csv("data/test_annofile.csv", header=None)
    to_write = add_gbk_annotations.annotate_gbk(gbk,anns)
    SeqIO.write(to_write, "output/annotated_gbk.gbk", "genbank")
    assert cmp("output/annotated_gbk.gbk","expected/annotated_gbk.gbk")