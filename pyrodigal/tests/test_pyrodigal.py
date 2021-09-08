import abc
import gzip
import os
import textwrap
import unittest
import warnings
from importlib.resources import open_binary

from pyrodigal import Pyrodigal, _api

from .fasta import parse


class _TestPyrodigalMode(object):

    mode = None

    @classmethod
    @abc.abstractmethod
    def find_genes(s):
        return NotImplemented

    # @classmethod
    # def setUpClass(cls):
    #     data = os.path.realpath(os.path.join(__file__, "..", "data"))
    #     fna = os.path.join(data, "SRR492066.fna.gz")
    #     meta_fna = os.path.join(data, "SRR492066.{}.fna.gz".format(cls.mode))
    #     meta_faa = os.path.join(data, "SRR492066.{}.faa.gz".format(cls.mode))
    #
    #     with gzip.open(fna, "rt") as f:
    #         cls.record = next(parse(f))
    #     with gzip.open(meta_faa, "rt") as f:
    #         cls.proteins = [
    #             record
    #             for record in parse(f)
    #             if record.id.startswith("{}_".format(cls.record.id))
    #         ]
    #     with gzip.open(meta_fna, "rt") as f:
    #         cls.genes = [
    #             record
    #             for record in parse(f)
    #             if record.id.startswith("{}_".format(cls.record.id))
    #         ]
    #
    #     cls.preds = cls.find_genes(str(cls.record.seq))
    #     cls.preds_bin = cls.find_genes(cls.record.seq.encode("ascii"))

    def assertTranslationsEqual(self, predictions, proteins):
        self.assertEqual(len(predictions), len(proteins))
        for pred, protein in zip(predictions, proteins):
            self.assertEqual(pred.translate(), str(protein.seq))

    def assertCoordinatesEqual(self, predictions, proteins):
        self.assertEqual(len(predictions), len(proteins))
        for gene, protein in zip(predictions, proteins):
            id_, start, end, strand, *_ = protein.description.split(" # ")
            self.assertEqual(gene.begin, int(start))
            self.assertEqual(gene.end, int(end))
            self.assertEqual(gene.strand, int(strand))

    def assertRbsMotifsEqual(self, predictions, proteins):
        self.assertEqual(len(predictions), len(predictions))
        for gene, protein in zip(predictions, proteins):
            *_, raw_data = protein.description.split(" # ")
            data = dict(keyval.split("=") for keyval in raw_data.split(";"))
            if data["rbs_motif"] != "None":
                self.assertEqual(gene.rbs_motif, data["rbs_motif"])
            else:
                self.assertIs(gene.rbs_motif, None)

    def assertStartTypesEqual(self, predictions, proteins):
        self.assertEqual(len(predictions), len(proteins))
        for gene, protein in zip(predictions, proteins):
            *_, raw_data = protein.description.split(" # ")
            data = dict(keyval.split("=") for keyval in raw_data.split(";"))
            self.assertEqual(gene.start_type, data["start_type"])

    def assertRbsSpacersEqual(self, predictions, proteins):
        self.assertEqual(len(predictions), len(proteins))
        for gene, protein in zip(predictions, proteins):
            *_, raw_data = protein.description.split(" # ")
            data = dict(keyval.split("=") for keyval in raw_data.split(";"))
            if data["rbs_spacer"] != "None":
                self.assertEqual(gene.rbs_spacer, data["rbs_spacer"])
            else:
                self.assertIs(gene.rbs_spacer, None)

    def test_translate_SRR492066(self):

        with gzip.open(open_binary("pyrodigal.tests.data", "SRR492066.fna.gz"), "rt") as f:
            record = next(parse(f))
        with gzip.open(open_binary("pyrodigal.tests.data", f"SRR492066.{self.mode}.faa.gz"), "rt") as f:
            proteins = [x for x in parse(f) if x.id.startswith("{}_".format(record.id))]

        preds = self.find_genes(str(record.seq))
        preds_bin = self.find_genes(record.seq.encode('ascii'))

        self.assertTranslationsEqual(preds, proteins)
        self.assertTranslationsEqual(preds_bin, proteins)

    # def test_coordinates_SRR492066(self):
    #     self.assertCoordinatesEqual(self.preds, self.proteins)
    #     self.assertCoordinatesEqual(self.preds_bin, self.proteins)
    #
    # def test_rbs_motif_SRR492066(self):
    #     self.assertRbsMotifsEqual(self.preds, self.proteins)
    #     self.assertRbsMotifsEqual(self.preds_bin, self.proteins)
    #
    # def test_rbs_spacer_SRR492066(self):
    #     self.assertRbsSpacersEqual(self.preds, self.proteins)
    #     self.assertRbsSpacersEqual(self.preds, self.proteins)
    #
    # def test_start_type_SRR492066(self):
    #     self.assertStartTypesEqual(self.preds, self.proteins)
    #     self.assertStartTypesEqual(self.preds_bin, self.proteins)


class TestPyrodigalMeta(_TestPyrodigalMode, unittest.TestCase):
    mode = "meta"

    @classmethod
    def find_genes(cls, seq):
        # return _api.find_genes_meta(seq)
        p = Pyrodigal(meta=True)
        return p.find_genes(seq)
#
#     def test_train(self):
#         p = Pyrodigal(meta=True)
#         self.assertRaises(RuntimeError, p.train, str(self.record.seq))
#
#     def test_overflow(self):
#         # > 180195.SAMN03785337.LFLS01000089
#         seq = """
#         AACCAGGGCAATATCAGTACCGCGGGCAATGCAACCCTGACTGCCGGCGGTAACCTGAAC
#         AGCACTGGCAATCTGACTGTGGGCGGTGTTACCAACGGCACTGCTACTACTGGCAACATC
#         GCACTGACCGGTAACAATGCGCTGAGCGGTCCGGTCAATCTGAATGCGTCGAATGGCACG
#         GTGACCTTGAACACGACCGGCAATACCACGCTCGGTAACGTGACGGCACAAGGCAATGTG
#         ACGACCAATGTGTCCAACGGCAGTCTGACGGTTACCGGCAATACGACAGGTGCCAACACC
#         AACCTCAGTGCCAGCGGCAACCTGACCGTGGGTAACCAGGGCAATATCAGTACCGCAGGC
#         AATGCAACCCTGACGGCCGGCGACAACCTGACGAGCACTGGCAATCTGACTGTGGGCGGC
#         GTCACCAACGGCACGGCCACCACCGGCAACATCGCGCTGACCGGTAACAATGCACTGGCT
#         GGTCCTGTCAATCTGAACGCGCCGAACGGCACCGTGACCCTGAACACAACCGGCAATACC
#         ACGCTGGGTAATGTCACCGCACAAGGCAATGTGACGACTAATGTGTCCAACGGCAGCCTG
#         ACAGTCGCTGGCAATACCACAGGTGCCAACACCAACCTGAGTGCCAGCGGCAATCTGACC
#         GTGGGCAACCAGGGCAATATCAGTACCGCGGGCAATGCAACCCTGACTGCCGGCGGTAAC
#         CTGAGC
#         """
#         p = Pyrodigal(meta=True, closed=False)
#         genes = p.find_genes(textwrap.dedent(seq).replace("\n", ""))
#         self.assertEqual(len(genes), 1)
#         self.assertEqual(genes[0].start_type, "Edge")
#         self.assertTrue(genes[0].partial_begin)
#         self.assertTrue(genes[0].partial_end)
#
#     def test_short_sequences(self):
#         seq = "AATGTAGGAAAAACAGCATTTTCATTTCGCCATTTT"
#         p = Pyrodigal(meta=True)
#         for i in range(1, len(seq)):
#             genes = p.find_genes(seq[:i])
#             self.assertEqual(len(genes), 0)
#             self.assertRaises(StopIteration, next, iter(genes))
#
#     def test_empty_sequence(self):
#         p = Pyrodigal(meta=True)
#         genes = p.find_genes("")
#         self.assertEqual(len(genes), 0)
#         self.assertRaises(StopIteration, next, iter(genes))
#
#     def test_unknown_letters(self):
#         # Commit 552721c fixed a bug where Pyrodigal was not correctly
#         # handling sequences of unknown letters, causing it to find genes
#         # inconsistently compared to Prodigal
#         data = os.path.realpath(os.path.join(__file__, "..", "data"))
#         src = os.path.join(data, "KK037166.fna.gz")
#         faa = os.path.join(data, "KK037166.{}.faa.gz".format(self.mode))
#
#         with gzip.open(src, "rt") as f:
#             record = next(parse(f))
#         with gzip.open(faa, "rt") as f:
#             proteins = [ record for record in parse(f) ]
#
#         predictions = self.find_genes(record.seq)
#         self.assertEqual(len(predictions), len(proteins))
#         for pred, protein in zip(predictions, proteins):
#             metadata = protein.description.split(" # ")
#             self.assertEqual(pred.begin, int(metadata[1]))
#             self.assertEqual(pred.end, int(metadata[2]))
#             self.assertEqual(pred.translate(), protein.seq)
#
#
# class TestPyrodigalSingle(_TestPyrodigalMode, unittest.TestCase):
#     mode = "single"
#
#     @classmethod
#     def find_genes(cls, seq):
#         p = Pyrodigal(meta=False)
#         with warnings.catch_warnings():
#             warnings.simplefilter("ignore")
#             p.train(seq)
#         return p.find_genes(seq)
#
#     def test_train_info(self):
#         p = Pyrodigal(meta=False)
#         with warnings.catch_warnings():
#             warnings.simplefilter("ignore")
#             info = p.train(self.record.seq)
#
#         self.assertEqual(info.translation_table, 11)
#         self.assertEqual(info.gc, 0.3010045159434068)
#         self.assertEqual(info.start_weight, 4.35)
#         self.assertEqual(info.bias[0], 2.6770525781861187)
#         self.assertEqual(info.bias[1], 0.17260535063729165)
#         self.assertEqual(info.bias[2], 0.1503420711765898)
#         self.assertEqual(info.type_weights[0], 0.71796361273324)
#         self.assertEqual(info.type_weights[1], -1.3722361344058844)
#         self.assertEqual(info.type_weights[2], -2.136731395763296)
#         self.assertTrue(info.uses_sd)
#
#
#     def test_train_not_called(self):
#         p = Pyrodigal(meta=False)
#         self.assertRaises(RuntimeError, p.find_genes, str(self.record.seq))
#
#     def test_training_info_deallocation(self):
#         p = Pyrodigal(meta=False)
#         with warnings.catch_warnings():
#             warnings.simplefilter("ignore")
#             p.train(str(self.record.seq))
#         genes = p.find_genes(str(self.record.seq))
#         del p # normally should not deallocate training info since it's RC
#         self.assertEqual(genes[0].translate(), str(self.proteins[0].seq))
#
#     def test_short_sequences(self):
#         seq = "AATGTAGGAAAAACAGCATTTTCATTTCGCCATTTT"
#         p = Pyrodigal(meta=False)
#         with warnings.catch_warnings():
#             warnings.simplefilter("ignore")
#             p.train(str(self.record.seq[:20000]))
#         for i in range(1, len(seq)):
#             genes = p.find_genes(seq[:i])
#             self.assertEqual(len(genes), 0)
#             self.assertRaises(StopIteration, next, iter(genes))
#
#     def test_empty_sequence(self):
#         p = Pyrodigal(meta=False)
#         with warnings.catch_warnings():
#             warnings.simplefilter("ignore")
#             p.train(str(self.record.seq[:20000]))
#         genes = p.find_genes("")
#         self.assertEqual(len(genes), 0)
#         self.assertRaises(StopIteration, next, iter(genes))
