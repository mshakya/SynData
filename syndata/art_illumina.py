#! /usr/bin/env python

"""Check design."""
from __future__ import print_function
import os
import luigi
from luigi import Parameter, LocalTarget, ExternalTask, ListParameter, DictParameter
from plumbum.cmd import art_illumina


def call_art_illumina(in_fasta, art_para_dic):
    """
    A function to run art illumina.

    This is a wrapper function for art_illumina
    """
    # list that are optional

    art_option_dic = {"amplicon": "--amplicon",
                      "cigarM": "--cigarM",
                      "delRate": "delRate",
                      "delRate2": "delRate2",
                      "errfree": "--errfree",
                      "fcov": "--fcov",
                      "insRate": "--insRate",
                      "insRate2": "--insRate2",
                      "len": "--len",
                      "mflen": "--mflen",
                      "matepair": "--matepair",
                      "noALN": "--noALN",
                      "out": "--out",
                      "paired": "--paired",
                      "qprof1": "--qprof1",
                      "qprof2": "--qprof2",
                      "qshift": "--qShift",
                      "qShift2": "--qShift2",
                      "rcount": "--rcount",
                      "rs": "--rndSeed",
                      "sdev": "--sdev",
                      "samout": "--samout",
                      "seqProf": "--seqProf",
                      "seqSys": "--seqSys"}

    # art_options = ["--in", in_fasta, "--out", in_fasta.split(".")[0]]
    art_options = ["--in", in_fasta]
    for key, value in art_para_dic.iteritems():
        if isinstance(value, bool):
            if value is True:
                art_options.append(art_option_dic[key])
            elif value is False:
                next
        else:
            flag = art_option_dic[key]
            art_options.append(flag)
            art_options.append(value)

    return art_options


class RefFile(ExternalTask):
    """An ExternalTask like this."""

    path = Parameter()

    def output(self):
        """Check."""
        return LocalTarget(os.path.abspath(self.path))


class RunArtIllumina(luigi.Task):
    """Running One istance of simulations.

    It simulates reads from one genome based on parameters given to the
    art_options
    """

    ref_fasta = Parameter()
    art_options = DictParameter()

    def requires(self):
        """Require fasta."""
        if isinstance(self.ref_fasta, str):
            return RefFile(self.ref_fasta)

    def output(self):
        """ART output."""
        paired = self.art_options['paired']
        if paired is True:
            out_file = self.art_options['out'] + "1.fq"
        else:
            out_file = self.art_options['out'] + ".fq"
        return LocalTarget(out_file)

    def run(self):
        """ART command."""
        art_options = call_art_illumina(in_fasta=self.ref_fasta, art_para_dic=self.art_options)
        art_cmd = art_illumina[art_options]
        art_cmd()


class RunAllArtIllumina(luigi.WrapperTask):
    """Generate synthetic data set for all."""

    ref_list = ListParameter()
    art_options = DictParameter()

    def requires(self):
        """A wrapper for running art illumina."""
        for ref_fasta in self.ref_list:
            yield RunArtIllumina(ref_fasta=ref_fasta, art_options=self.art_options)
