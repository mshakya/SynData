#!/usr/bin/env python

"""Tests for `syndata` package."""

from __future__ import print_function
import pytest
from syndata import call_art_illumina


def test_call_art_illumina():
    x = call_art_illumina(IN="test.fna", out="migun")
    print(x)
    assert len(x) == 10

def test_call_art_illumina2():
    x = call_art_illumina(IN="data/E_coli.fasta", out="out_data")
    assert x == ['--in', 'data/E_coli.fasta', '--seqSys', 'MSv1', '--len', 250, '--fcov', 10, '--out', 'migun']
