# Test scripts


## Requirements
* MacOS, Linux
* make
* python3
* sqlite >= 3.17
* taxadb python module has been set up

## Configuration
1. Create the virtual environment: `make .env` . This is done once per checkout
2. Enable the virtual environment: `source .env/bin/activate`. This is done once per session
3. Configure taxadb: `make init_taxadb`. This is done once per installation.
3. Set the `TAXADB_CONFIG` environment variable: `export TAXADB=${PWD}/etc/taxadb.cfg`. This is done once per session
4. Make sure you download the taxidlineage.dmp to data directory: `make taxidlineage.dmp`

## Instructions
1. Check out source tree
   `git clone https://github.com/NCBI-Codeathons/Taxonomy-specific-RPS-BLAST-part-I.git`
2. `cd Taxonomy-specific-RPS-BLAST-part-I/src`
3. `make init_taxadb check`
4. To compute the trees for all sample files, run `make all`


## To experiment

To run the test script, one must enable the virtual environment *and* set the
`TAXADB_CONFIG` environment variable (see Configuration section above). Then,
run the script as follows:

   `./dtrt.py <data/*.tsv-file-name> -show_tree [-threshold <number-between-0-and-1> ]`


### dtrt.py options

* `-threshold`: Threshold to report taxonomy node.
    Default value: 0.95
* `-show_tree`: Display taxonomy tree for model.
    Default value: false
* `-shake`: Experimental: 'shakes' the tree to remove nodes that contribute
  less than 1% to the parent's weight.
    Default value: false

