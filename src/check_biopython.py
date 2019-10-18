#!/usr/bin/env python3
"""
check_biopython.py - See DESC constant below

Author: Christiam Camacho (camacho@ncbi.nlm.nih.gov)
Created: Fri 18 Oct 2019 12:47:33 PM EDT
"""

from Bio import Entrez

def main():
    """ Entry point into this program. """
    Entrez.email = "ccamacho@nih.gov"
    for taxid in sys.argv[1:]:
        print("Processing taxid {}".format(taxid))
        handle = Entrez.efetch(db="Taxonomy", id=str(taxid), retmode="xml")
        records = Entrez.read(handle)
        if len(records) != 1:
            print("Retrieved {} records, skipping".format(len(records)))
            continue
        #print(records[0].keys())
        print("\tSci_name {}".format(records[0]["ScientificName"]))
        print("\tLineage {}".format(records[0]["Lineage"]))


    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

