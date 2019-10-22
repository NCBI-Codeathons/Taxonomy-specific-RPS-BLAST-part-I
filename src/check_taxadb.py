#!/usr/bin/env python3
import sys
from taxadb.taxid import TaxID

taxid = TaxID()
for t in sys.argv[1:]:
    name = taxid.sci_name(int(t))
    print(name)
