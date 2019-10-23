# Test scripts

[![Build Status](https://travis-ci.org/christiam/Taxonomy-specific-RPS-BLAST-part-I.svg?branch=master)](https://travis-ci.org/christiam/Taxonomy-specific-RPS-BLAST-part-I)


## Requirements
* MacOS, Linux
* make
* python3
* sqlite >= 3.17

## Instructions
1. Check out source tree
   `git clone https://github.com/NCBI-Codeathons/Taxonomy-specific-RPS-BLAST-part-I.git`
2. `cd Taxonomy-specific-RPS-BLAST-part-I/src`
3. `make init_taxadb check`
4. To compute the trees for all sample files, run `make all`


## To experiment

To run the test script, one must enable the virtual environment *and* set the
`TAXADB_CONFIG` environment variable:

1. Create the virtual environment: `make .env` . This is done once per
   checkout
2. Enable the virtual environment: `source .env/bin/activate`. This is done
   once per session
3. Set the `TAXADB_CONFIG` environment variable: `export TAXADB=${PWD}/etc/taxadb.cfg`. This is done
   once per session
4. Make sure you download the taxidlineage.dmp to data directory, i.e. `curl -o data/taxidlineage.dmp ftp://ftp.ncbi.nlm.nih.gov/blast/temp/model2taxid/taxidlineage.dmp`
5. Run the script 
   `./dtrt.py <data/*.tsv-file-name> -show_tree [-threshold <number-between-0-and-1> ]`


## dtrt.py options

* `-threshold`: Threshold to report taxonomy node.
    Default value: 0.95
* `-show_tree`: Display taxonomy tree for model.
    Default value: false
* `-shake`: Experimental: 'shakes' the tree to remove nodes that contribute
  less than 1% to the parent's weight.
    Default value: false
* `-use_eutils`: Use e-Utils to resolve taxonomic names
    Default value: false

  

