#!/usr/bin/env python

"""Tests for `syndata` package."""

from __future__ import print_function
import pytest
from syndata import art_illumina


def test_call_art_illumina():
    """
    Test call_art_illumina outputs right set of option.

    this only test if the function parses it correctly
    """
    x = art_illumina.call_art_illumina(in_fasta="test.fna", art_para_dic={"errfree": True,
                                                             "paired": True,
                                                             "fcov": 11})
    assert len(x) == 6

def test_call_art_illumina2():
    """
    Test call_art_illumina outputs right set of option.

    this only test if the function parses it correctly
    """

    x = art_illumina.call_art_illumina(in_fasta="data/E_coli.fasta", art_para_dic={"seqSys": "MSv1",
                                                                 "paired": True,
                                                                 "fcov": 11,
                                                                 "len": 250})
    assert 'MSv1' in ['--in', 'data/E_coli.fasta', '--seqSys', 'MSv1', '--paired',
                      '--fcov', '11', '--len', 250]
