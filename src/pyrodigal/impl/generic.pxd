# coding: utf-8
# cython: language_level=3, linetrace=True, binding=True

from ..lib cimport BaseConnectionScorer

cdef class GenericConnectionScorer(BaseConnectionScorer):
    pass