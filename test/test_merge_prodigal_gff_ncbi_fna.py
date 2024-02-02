import merge_prodigal_gff_ncbi_fna
from Bio import SeqIO
from filecmp import cmp

def test_merge():
    merge_prodigal_gff_ncbi_fna.merge("data/test_multirecord_assembly.fna", "data/test_multirecord_assembly.gff", "output/test_out_merge_fna_gff.gbk")
    assert cmp("output/test_out_merge_fna_gff.gbk",  "expected/expected_out_merge_fna_gff.gbk")
