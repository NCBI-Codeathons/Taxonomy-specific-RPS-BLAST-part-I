#!/usr/bin/env python3
"""
dtrt.py - See DESC constant below

Created: Thu Oct 17 14:51:30 2019
"""
import argparse
import unittest
import logging
import os
from taxtree.tree import createTree

VERSION = '0.1'
DFLT_LOGFILE = 'notebook.log'
DESC = r"""Domain-to-Taxonomy Research Tool"""


class Tester(unittest.TestCase):
    """ Testing class for this script. """
    def test_one(self):
        self.assertTrue(1)


def load_taxonomy_lineage():
    lineage_file = 'data/taxidlineage.dmp'
    lin_dict = {}
    lin_dict['taxid'] = 00000

    with open(lineage_file, 'r') as fh:
        for line in fh:
            lst = line.split('|')
            lin_dict[lst[0].strip('\t')] = lst[1].strip('\t').strip()

    return lin_dict

def get_lineages_for_model_components(tsv_file_with_model_component_data, lineage):
    # Marc
    # input: domgi	accession	taxid	taxOrg	nPig	nGi
    # 200311	TIGR03687	1883	Streptomyces	131	605
    # output:
    # (taxid, nPIG/weight, lineage)
    lin_lst = []

    for line in tsv_file_with_model_component_data:
        tmp = line.split('\t')
        try:
            lin_lst.append((tmp[2], int(tmp[4]), lineage[tmp[2]].split()))
        except:
            # if taxid not in dictionary, skip
            pass

    return lin_lst


def get_taxids_from_model(tsv_file_with_model_component_data):
    """ Function to extract taxIDs from a file containing model taxonomic data """
    retval = []
    for line_no, line in enumerate(tsv_file_with_model_component_data, 1):
        try:
            retval.append(int(line.split('\t')[2]))
        except:
            logging.warn("Failed to parse line " + line_no)

    return retval

def main():
    """ Entry point into this program. """
    parser = create_arg_parser()
    args = parser.parse_args()
    config_logging(args)

    tax_lineage = load_taxonomy_lineage()
    tuples = get_lineages_for_model_components(args.model_component_data, tax_lineage)

    if args.show_names:
        os.environ["GET_NAMES_FROM_ENTREZ"] = "1"

    tree = createTree(tuples)
    tree.describe()

    if args.show_tree:
        print(tree)

    if args.shake:
        print("after shaking, the tree status is below: ")
        tree.shake()

    print("lowest common node:")
    print(tree.lowestCommonNode())
    print("potential outlier:")
    print(tree.potentialOutlier())
    print(tree.report(args.threshold))
    return 0


def create_arg_parser():
    """ Create the command line options parser object for this script. """
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("model_component_data", type=argparse.FileType('r'))
    parser.add_argument("-threshold", type=float,
                        help="Threshold to report taxonomy node, default=.95",
                        default=.95)
    parser.add_argument("-logfile", default=DFLT_LOGFILE,
                        help="Default: " + DFLT_LOGFILE)
    parser.add_argument("-show_tree", action='store_true',
                        help="Display taxonomy tree for model")
    parser.add_argument("-show_names", action='store_true',
                        help="Display taxonomic names instead of just taxids")
    parser.add_argument("-shake", action='store_true',
                        help="Experimental: 'shakes' the tree to remove nodes that contribute less than 1%% to the parent's weight")
    parser.add_argument("-loglevel", default='INFO',
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s ' + VERSION)
    return parser


def config_logging(args):
    if args.logfile == 'stderr':
        logging.basicConfig(level=str2ll(args.loglevel),
                            format="%(asctime)s %(message)s")
    else:
        logging.basicConfig(filename=args.logfile, level=str2ll(args.loglevel),
                            format="%(asctime)s %(message)s", filemode='w')
    logging.logThreads = 0
    logging.logProcesses = 0
    logging._srcfile = None


def str2ll(level):
    """ Converts the log level argument to a numeric value.

    Throws an exception if conversion can't be done.
    Copied from the logging howto documentation
    """
    retval = getattr(logging, level.upper(), None)
    if not isinstance(retval, int):
        raise ValueError('Invalid log level: %s' % level)
    return retval


if __name__ == "__main__":
    import sys
    sys.exit(main())

