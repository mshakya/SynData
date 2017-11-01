#! /usr/bin/env python

"""Generate distribution of various kind representing relative abundance."""
from __future__ import print_function
import numpy as np


def gen_dist(ref_list, dist):
    """Generate distribution of various kind representing relative abundance.

    It takes in list of refernce , name of distribution, from
    selected few, and outputs a dictionary with reference name
    and corresponding coverage information.

    """
    rel_abun_dic = {}
    no_of_ref = len(ref_list)
    if dist == "log-normal":
        random_nos = np.random.lognormal(5, 2.5, no_of_ref)
        total = np.sum(random_nos)
        rel_abun = random_nos / total
    if dist == "equal":
        random_nos = np.ones(no_of_ref)
        rel_abun = random_nos / no_of_ref
    if dist == "log":
        random_nos = np.random.logistic(5, 2.5, no_of_ref)
        total = np.sum(random_nos)
        rel_abun = random_nos / total
    if dist == "normal":
        random_nos = np.random.normal(5, 2.5, no_of_ref)
        total = np.sum(random_nos)
        rel_abun = random_nos / total
    rel_abun_dic = dict(zip(ref_list, rel_abun))
    return rel_abun_dic

