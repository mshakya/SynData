#! /usr/bin/env python

"""Run Art Illumina."""
from __future__ import print_function
import os
import re
import luigi
import shutil
from luigi import Parameter, LocalTarget, ExternalTask, ListParameter, DictParameter, BoolParameter
from luigi.util import requires
from plumbum.cmd import art_illumina, cat
from syndata import coverage


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

    art_options = ["--in", in_fasta]
    for key, value in art_para_dic.items():
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
    out_dir = Parameter()

    def requires(self):
        """Require fasta."""
        if isinstance(self.ref_fasta, str):
            return RefFile(self.ref_fasta)

    def output(self):
        """ART output."""
        out_dir = os.path.abspath(self.out_dir)
        paired = self.art_options['paired']
        if paired is True:
            out_file = os.path.join(out_dir, self.ref_fasta.split(".")[0] + "1.fq")
        else:
            out_file = os.path.join(out_dir, self.ref_fasta.split(".")[0] + ".fq")
        return LocalTarget(out_file)

    def run(self):
        """ART command."""
        art_options = call_art_illumina(in_fasta=self.ref_fasta, art_para_dic=self.art_options)
        art_cmd = art_illumina[art_options]
        art_cmd()
        move_files("fq", os.getcwd(), os.path.abspath(self.out_dir))
        if self.art_options['samout'] is True:
            move_files("sam", os.getcwd(), os.path.abspath(self.out_dir))
        if self.art_options['noALN'] is False:
            move_files("aln", os.getcwd(), os.path.abspath(self.out_dir))


class RunAllArtIllumina(luigi.WrapperTask):
    """Generate synthetic data set for all."""

    ref_list = ListParameter()
    art_options = DictParameter()
    metagenome = BoolParameter(default=False)
    distribution = Parameter()
    out_dir = Parameter()

    def requires(self):
        """A wrapper for running art illumina."""
        if self.metagenome is False:
            for ref_fasta in self.ref_list:
                yield RunArtIllumina(ref_fasta=ref_fasta, art_options=self.art_options)
        elif self.metagenome is True:
            cov_dic = coverage.gen_dist(self.ref_list, self.distribution)
            art_options_dic = dict(self.art_options)
            for ref_fasta in self.ref_list:
                art_options_dic['fcov'] = cov_dic[ref_fasta]
                art_options_dic['out'] = re.split('.fasta|.fna', os.path.basename(ref_fasta))[0]
                yield RunArtIllumina(ref_fasta=ref_fasta,
                                     art_options=art_options_dic,
                                     out_dir=self.out_dir)


@requires(RunAllArtIllumina)
class MergeSynFiles(luigi.Task):
    """Merge the generate synthetic dataset to represent one Metagenome."""

    metagenome = BoolParameter()
    metagenome_options = DictParameter()
    art_options = DictParameter()
    out_dir = Parameter()

    def output(self):
        """Define expected ouputs."""
        out_dir = os.path.abspath(self.out_dir)
        paired = self.art_options['paired']
        out_prefix = self.metagenome_options['metagenome_prefix']
        if paired is True:
            fr = os.path.join(out_dir, out_prefix + "R2.fq")
        elif paired is False:
            fr = os.path.join(out_dir, out_prefix + ".fq")
        return LocalTarget(fr)

    def run(self):
        """Concatenate files from all simulations."""
        out_dir = os.path.abspath(self.out_dir)
        out_dir_files = os.listdir(out_dir)
        if self.metagenome is True:
            out_prefix = self.metagenome_options['metagenome_prefix']
            if self.art_options['paired'] is True:
                fq1_list = []
                fq2_list = []
                for fq in out_dir_files:
                    fq = os.path.join(out_dir, fq)
                    if fq.endswith("fq"):
                        if "1.fq" in fq:
                            fq1_list.append(fq)
                        elif "2.fq" in fq:
                            fq2_list.append(fq)
                fq1_files = sorted(fq1_list)
                fq1_out = os.path.join(out_dir, out_prefix + "R1.fq")
                fq2_files = sorted(fq2_list)
                fq2_out = os.path.join(out_dir, out_prefix + "R2.fq")
                cat_fq1_cmd = cat[fq1_files] > fq1_out
                cat_fq2_cmd = cat[fq2_files] > fq2_out
                cat_fq1_cmd()
                cat_fq2_cmd()
            elif self.art_options['paired'] is False:
                fq_list = []
                for fq in out_dir_files:
                    fq = os.path.join(out_dir, fq)
                    if fq.endswith(".fq"):
                        fq_list.append(fq)
                fq_out = os.path.join(out_dir, out_prefix + ".fq")
                cat_fq_cmd = cat[fq_list] > fq_out
                cat_fq_cmd()
            if self.art_options['samout'] is True:
                errfree_sams = []
                regular_sams = []
                for sam in out_dir_files:
                    sam = os.path.join(out_dir, sam)
                    if sam.endswith("sam"):
                        if "errFree" in sam:
                            errfree_sams.append(sam)
                        else:
                            regular_sams.append(sam)
                reg_cat_files = os.path.join(out_dir, out_prefix + ".sam")
                ef_cat_files = os.path.join(out_dir, out_prefix + "_errFree.sam")
                cat_reg_cmd = cat[regular_sams] > reg_cat_files
                cat_ef_cmd = cat[errfree_sams] > ef_cat_files
                cat_reg_cmd()
                cat_ef_cmd()

            if self.art_options['noALN'] is False:
                aln_files = []
                for aln in os.listdir(self.out_dir):
                    if aln.endswith("aln"):
                        aln_files.append(aln)

        elif self.metaganome is False:
            pass


def move_files(ext, source, dest):
    """A simple function that iteratively moves that have given extension."""
    for file in os.listdir(source):
        if file.endswith(ext):
            shutil.move(file, dest)
