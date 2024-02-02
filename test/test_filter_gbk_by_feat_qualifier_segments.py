import filter_gbk_by_feat_qualifier_segments
from Bio import SeqIO
from filecmp import cmp

# TODO test against multiple 'by' and keep criteria
def test_filter_gbk():
    filter_gbk_by_feat_qualifier_segments.filter_gbk("data/test_multirecord_assembly.gbk",
                                                     "ID",
                                                     ["1_2","1_4","10_4","42_5"],
                                                     "output/filter_gbk_segments.gbk")
    assert cmp("output/filter_gbk_segments.gbk","expected/filter_gbk_segments.gbk")
