# Test scripts


## Requirements
* MacOS, Linux
* make
* python3

## Instructions
1. Check out source tree
   `git clone https://github.com/NCBI-Codeathons/Taxonomy-specific-RPS-BLAST-part-I.git`
2. `cd Taxonomy-specific-RPS-BLAST-part-I/src`
3. `make check`


## To experiment

To run the test script, one must enable the virtual environment:

1. Create the virtual environment: `make .env` . This is done once per
   checkout
2. Enable the virtual environment: `source .env/bin/activate`. This is done
   once per session
3. Make sure you download the taxidlineage.dmp to data directory, i.e. `curl -o data/taxidlineage.dmp ftp://ftp.ncbi.n
lm.nih.gov/blast/temp/model2taxid/taxidlineage.dmp`
4. Run the script 
   `./dtrt.py <data/*.tsv-file-name> [-threshold <number-between-0-and-1> ]`


## dtrt.py options

* `-threshold`: Threshold to report taxonomy node.
    Default value: 0.95
* `-show_names`: Display taxonomic names instead of just taxids.
    Default value: false
* `-show_tree`: Display taxonomy tree for model.
    Default value: false
* `-shake`: Experimental: 'shakes' the tree to remove nodes that contribute
  less than 1% to the parent's weight.
    Default value: false

  

