from pyrodigal.prodigal.bitmap cimport bitmap_t
from pyrodigal.prodigal.sequence cimport _mask
from pyrodigal.prodigal.training cimport _training


cdef extern from "node.h" nogil:

    const size_t STT_NOD
    const size_t MIN_GENE
    const size_t MIN_EDGE_GENE
    const size_t MAX_SAM_OVLP
    const size_t ST_WINDOW
    const size_t OPER_DIST
    const double EDGE_BONUS
    const double EDGE_UPS
    const double META_PEN

    struct _motif:
        int ndx
        int len
        int spacer
        int spacendx
        double score

    struct _node:
        int type
        bint edge
        int ndx
        int strand
        int stop_val
        int star_ptr[3]
        int gc_bias
        double gc_score[3]
        double cscore
        double gc_cont
        int rbs[2]
        _motif mot
        double uscore
        double tscore
        double rscore
        double sscore
        int traceb
        int tracef
        int ov_mark
        double score
        int elim

    int add_nodes(bitmap_t seq, bitmap_t rseq, int slen, _node* nodes, bint closed, _mask* mlist, int nm, _training* tinf) noexcept
    void reset_node_scores(_node*, int) noexcept
    int compare_nodes(const void*, const void*) noexcept
    int stopcmp_nodes(const void*, const void*) noexcept

    void record_overlapping_starts(_node*, int, _training*, int) noexcept
    void record_gc_bias(int*, _node*, int, _training*) noexcept

    void calc_dicodon_gene(_training*, unsigned char*, unsigned char*, int, _node*, int) noexcept
    void calc_amino_bg(_training*, unsigned char*, unsigned char*, int, _node*, int) noexcept

    void score_nodes(unsigned char*, unsigned char*, int, _node*, int, _training*, int, int) noexcept
    void calc_orf_gc(unsigned char*, unsigned char*, int, _node*, int, _training*) noexcept
    void rbs_score(unsigned char*, unsigned char*, int, _node *, int, _training*) noexcept
    void score_upstream_composition(unsigned char*, int, _node*, _training*) noexcept

    void raw_coding_score(bitmap_t seq, bitmap_t rseq, int slen, _node *nod, int nn, _training *tinf) noexcept

    void determine_sd_usage(_training *tinf) noexcept

    double intergenic_mod(_node*, _node*, _training*) noexcept

    void train_starts_sd(bitmap_t seq, bitmap_t rseq, int slen, _node *nodes, int nn, _training *tinf) noexcept
    void train_starts_nonsd(bitmap_t seq, bitmap_t rseq, int slen, _node *nodes, int nn, _training *tinf) noexcept

    void count_upstream_composition(unsigned char*, int, int, int, _training*) noexcept

    void build_coverage_map(double[4][4][4096], int[4][4][4096], double, int) noexcept
    void find_best_upstream_motif(_training*, unsigned char*, unsigned char*, int, _node*, int) noexcept
    void update_motif_counts(double[4][4][4096], double*, unsigned char*, unsigned char*, int, _node*, int) noexcept

    bint cross_mask(int, int, _mask*, int) noexcept

    double dmax(double, double) noexcept
    double dmin(double, double) noexcept
