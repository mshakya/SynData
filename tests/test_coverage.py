#!/usr/bin/env python

"""Tests for `syndata` package."""

from __future__ import print_function
import pytest
from syndata import coverage


def test_gen_dist():
    """
    Test gen_dist function.

    this test checks if you give 4 files, it gives dictionary of length 4
    if the relative abundance adds upto 1
    """
    ref_list = ["test1.fasta", "test2.fna", "test3.fasta", "test4.fa"]
    x = coverage.gen_dist(ref_list, dist="equal")
    sum_x = sum(x.values())
    assert sum_x == 1
    assert len(x) == 4
