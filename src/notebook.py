#!/usr/bin/env python2
"""
notebook.py - See DESC constant below

Created: Thu Oct 17 14:51:30 2019
"""
import argparse
import unittest
import logging
from ete3 import Tree, NCBITaxa, PhyloTree, TreeStyle, TextFace

VERSION = '0.1'
DFLT_LOGFILE = 'notebook.log'
DESC = r"""\
DESCRIPTION GOES HERE
"""


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

    ncbi_taxserver = NCBITaxa()

    t = Tree()
    taxids = get_taxids_from_model(args.model_component_data)
    lineages = ncbi_taxserver.get_lineage_translator(taxids)

    print "Number of taxids", len(taxids)
    print "First taxid", taxids[0]
    print "First lineage", lineages[taxids[0]]

    tree = PhyloTree(sp_naming_function=lambda name: name)

    ### # Check the data fetched by ete3.NCBITaxa
    ### for i, (taxid, lineage) in enumerate(lineages.items()):
    ###     if i < 1:
    ###         print "taxid", taxid
    ###         print "lineage", lineage

    print "Empty", tree.get_ascii(show_internal=True)
    x = tree
    m = x.add_child(name=10090)
    h = x.add_child(name=207598)
    h.add_child(name=9606)
    h.add_child(name=9598)

    #x = tree.add_child(name=1)
    #x = tree.add_child(name=131567)
    #x = x.add_child(name=2)
    print "After 2 levels", tree.get_ascii()
    #x = x.add_child(name=1224)
    #x = x.add_child(name=28211)
    #x = x.add_child(name=356)
    #print "After 5 levels", tree.get_ascii()
    #x = x.add_child(name=69277)
    #x = x.add_child(name=68287)
    #x = x.add_child(name=325217)
    #x = x.add_child(name=1871066)
    #print tree.get_ascii(show_internal=True)

    tax2names, tax2lineages, tax2rank = tree.annotate_ncbi_taxa()
    print "tax2names", type(tax2names), "n=", len(tax2names)#, "131567=", tax2names[131567]
    print "tax2lineages", type(tax2lineages), "n=", len(tax2lineages)#, "131567=", tax2lineages[131567]
    print "tax2rank", type(tax2rank), "n=", len(tax2rank)#, "131567=", tax2rank[131567]

    print "DEMO HERE **************"
    demo_tree = PhyloTree('((9606, 9598), 10090);', sp_naming_function=lambda name: name)
    tax2names, tax2lineages, tax2rank = demo_tree.annotate_ncbi_taxa()
    print "tax2names", type(tax2names), "n=", len(tax2names)#, "131567=", tax2names[131567]
    print "tax2lineages", type(tax2lineages), "n=", len(tax2lineages)#, "131567=", tax2lineages[131567]
    print "tax2rank", type(tax2rank), "n=", len(tax2rank)#, "131567=", tax2rank[131567]
    print "DEMO tax2names **************"
    print tax2names

    # for taxid in taxids:
    #     lineage = ncbi_taxserver.get_lineage_translator(taxid)

    # lineage = load_taxonomy_lineage()
    # component_data = get_lineages_for_model_components(args.model_component_data, lineage)
    # for n, tuple in enumerate(component_data):
    #     if n < 1:
    #         print "taxid", tuple[0]
    #         print "weight (numIPGs)", tuple[1]
    #         print "lineage", tuple[2]
    #         child = t
    #         for node in tuple[2]:
    #             child = child.add_child(name=node, taxid=node)
    #         child.add_child(tuple[0])
    #         print

    print demo_tree.get_ascii(attributes=['sci_name', 'taxid'])
    ts = TreeStyle()
    ts.show_leaf_name = True
    ts.title.add_face(TextFace("Tree for " + str(taxids[0]), fsize=20), column=0)
    demo_tree.render("notebook.png", w=400, tree_style=ts)



    return 0


def create_arg_parser():
    """ Create the command line options parser object for this script. """
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("model_component_data", type=argparse.FileType('r'))
    parser.add_argument("-logfile", default=DFLT_LOGFILE,
                        help="Default: " + DFLT_LOGFILE)
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

