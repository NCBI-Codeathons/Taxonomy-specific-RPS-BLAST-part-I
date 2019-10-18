# Taxonomy-specific-RPS-BLAST-part-I
Protein is usually made up of domain(s). Conserved Domains can be described by local multiple sequence alignments spanning a variety of organisms to reveal sequence regions that contain the same, or similar, patterns of amino acids. Although it is easy to retrieve the taxonomical distribution of a protein, it is not available at the domain level.

This 2019 NCBI-Codeathon project will develop a pipeline to assign a lowest common taxid to a conserved protein domain (defined by a Position-Specific Score Matrix, [PSSM](https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd_help.shtml#CD_PSSM)). The taxid represents the taxon that contains this domain specifically with given threshold. This project will be incorporated into the future [RPS-Blast](https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd_help.shtml#RPSBWhat) (RPS-BLAST uses the query sequence to search a database of pre-calculated PSSMs, and report significant hits) to provide taxonomic information in [CD Search](https://www.ncbi.nlm.nih.gov/Structure/cdd/wrpsb.cgi) (Conserved Domain Search) results.

![alt text](https://github.com/NCBI-Codeathons/Taxonomy-specific-RPS-BLAST-part-I/blob/master/Presentation/image1008.png)
## Dependencies:
Python 3

BioPython

NCBI [Conserved Domain Architecture Retrieval Tool (CDART)](https://www.ncbi.nlm.nih.gov/Structure/lexington/docs/cdart_help.html)

taxidlineage.dmp extracted from new_taxdump.zip available in NCBI Taxonomy ftp site (ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/)

## Workflow:
![alt text](https://github.com/NCBI-Codeathons/Taxonomy-specific-RPS-BLAST-part-I/blob/master/Presentation/workflow.png)
### Input: 

A table generate by [sql query](https://github.com/NCBI-Codeathons/Taxonomy-specific-RPS-BLAST-part-I/blob/master/utilities/get-model-component-taxonomy.sh) against NCBI internal CDART database ([example file](https://github.com/NCBI-Codeathons/Taxonomy-specific-RPS-BLAST-part-I/blob/master/src/data/pfam10339-components.tsv))

### Command:
`./notebook.py <data/*.tsv-file-name> [-threshold <number-between-0-and-1>0]`
  
  options:
  
- -threshold: Threshold to report taxonomy node. Default value: 0.95
   
- -show_names: Display taxonomic names instead of just taxids. Default value: false
   
- -show_tree: Display taxonomy tree for model. Default value: false
   
- -shake: Experimental: 'shakes' the tree to remove nodes that contribute less than 1% to the parent's weight. Default value: false

### Output: 
[A taxonomy tree with the lowest common taxid with the threshold for the domain](https://github.com/NCBI-Codeathons/Taxonomy-specific-RPS-BLAST-part-I/blob/master/results/pfam10339_95.txt)

## Validation:
PSSM-Id: 129695,200311,334026,334050,337780,335786,274086,308214,315456,338615,287328,313550,313551,274263


## FAQ
## People/Team
Marc Gwadz, IEB/NCBI/NIH

Christiam Camacho, IEB/NCBI/NIH

Jianli Dai, IEB/NCBI/NIH

Hanguan Liu, IEB/NCBI/NIH

Mingzhang Yang, IEB/NCBI/NIH

