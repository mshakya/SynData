#! /usr/bin/env python

"""Check design."""
from __future__ import print_function

def call_art_illumina(IN, out,
                      paired=None,
                      qprof1=None,
                      qprof2=None,
                      amp=None,
                      rcount=None,
                      id=None,
                      errfree=None,
                      fcov=10,
                      insRate=0.00009,
                      insRate2=0.00015,
                      delRate=0.00011,
                      delRate2=0.00023,
                      maxIndel=None,
                      length=250,
                      mflen=None,
                      matepair=None,
                      cigarM=None,
                      maskN=None,
                      noALN=None,
                      minQ=None,
                      maxQ=None,
                      qShift=None,
                      qShift2=None,
                      rndSeed=None,
                      sdev=None,
                      samout=None,
                      sepProf=None,
                      seqSys="MSv1"):
    """
    A function to run art illumina.

    This is a wrapper function for art_illumina
    """

    # list that are optional
    optional_list = filter(None, [qprof1, qprof2, rcount])

    boolean_dict = {amp: "--amplicon", errfree: "--errfree",
                    cigarM: "--cigarM", noALN: "--noALN",
                    paired: "--paired", samout: "--samout",
                    sepProf: "--sepProf", matepair: "--matepair"}

    boolean_list = filter(None, [amp, errfree, cigarM, noALN, matepair, paired, samout, sepProf])

    used_boolean_list = []
    for x in boolean_list:
        if x is True:
            used_boolean_list.append(boolean_dict[x])

    used_default_list = []
    default_list = filter(None, [insRate, insRate2, delRate, delRate2, maxIndel])
    default_option_dict = {insRate: ["--insRate", insRate],
                    insRate2: ["--insRate2", insRate2],
                    delRate: ["--delRate", delRate],
                    delRate2: ["--delRate2", delRate2]}
    for x in default_list:
        used_default_list.append(default_option_dict[x])



    command = ["--in", IN,
               "--seqSys", seqSys,
               "--len", length,
               "--fcov", fcov,
               "--out", out] + used_boolean_list + optional_list
    print(command)
    return command
