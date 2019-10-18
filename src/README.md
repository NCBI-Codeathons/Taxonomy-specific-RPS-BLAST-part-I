# Test scripts


## Requirements
* MacOS
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
3. Run the script 
   `./notebook.py <data/*.tsv-file-name> [-threshold <number-between-0-and-1>0]`


## notebook.py options

* `-threshold`: 
    Default value: 0.95
* `-show_names`: 
    Default value: false
* `-show_tree`:
    Default value: false
* `-shake_tree`:
    Default value: false

  

