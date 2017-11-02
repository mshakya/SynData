#!/usr/bin/env python

"""Tests for `syndata` package."""

from __future__ import print_function
import pytest
import luigi
import os
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

def test_RunArtIlluminaPaired(tmpdir):
    """
    Test if this first luigi class works

    this is a way to test a class of luigi

    """
    luigi.interface.build([art_illumina.RunArtIllumina(ref_fasta="tests/data/E_coli.fasta", 
                                                       art_options={'paired':True, 'samout': True,
                                                       'noALN':True, 'mflen': 2000, 'sdev': 10, 'errfree':True,
                                                       'seqSys':'MS', 'len': 200, 'out': 'test', 'fcov': 2},
                                                       out_dir=tmpdir)],
                          local_scheduler=True, workers=1)
    file_basenames = [os.path.basename(x) for x in tmpdir.listdir()] 
    assert 'test_errFree.sam' in file_basenames
    assert 'test.sam' in file_basenames
    assert 'test1.fq' in file_basenames
    assert 'test2.fq' in file_basenames

def test_RunArtIlluminaSingle(tmpdir):
    """
    Test if this first luigi class works

    this is a way to test a class of luigi

    """
    luigi.interface.build([art_illumina.RunArtIllumina(ref_fasta="tests/data/E_coli.fasta", 
                                                       art_options={'paired': False, 'samout': True,
                                                       'noALN':True, 'mflen': 1000, 'sdev': 10, 'errfree':True,
                                                       'seqSys':'MS', 'len': 200, 'out': 'test', 'fcov': 2},
                                                       out_dir=tmpdir)],
                          local_scheduler=True, workers=1)
    s = tmpdir.join("test.sam")
    assert len(tmpdir.listdir()) == 4
    file_basenames = [os.path.basename(x) for x in tmpdir.listdir()] 
    assert 'test_errFree.sam' in file_basenames
    assert 'test.sam' in file_basenames
    assert 'test1.fq' in file_basenames
