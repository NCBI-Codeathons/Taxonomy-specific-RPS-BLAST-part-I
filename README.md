# Taxonomy-specific-RPS-BLAST-part-I
Protein is usually made up of domain(s). Conserved Domains can be described by local multiple sequence alignments spanning a variety of organisms to reveal sequence regions that contain the same, or similar, patterns of amino acids. Although it is easy to retrieve the taxonomical distribution of the protein, it is not available at the domain level.

This 2019 NCBI-Codeathon project will develop a pipeline to assign a taxonomy id to a conserved protein domain (defined by a Position-Specific Score Matrix, [PSSM](https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd_help.shtml#CD_PSSM)). The taxonomy id represents the taxon that contains this domain specifically. This project will be incorporated into future [RPS-Blast](https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd_help.shtml#RPSBWhat) (RPS-BLAST uses the query sequence to search a database of pre-calculated PSSMs, and report significant hits in a single pass) to provide taxonomy information in [CD Search](https://www.ncbi.nlm.nih.gov/Structure/cdd/wrpsb.cgi) (Conserved Domain Search) results.

![alt text](https://github.com/NCBI-Codeathons/Taxonomy-specific-RPS-BLAST-part-I/blob/master/Presentation/image1008.png)
## Dependencies:
Python 3

NCBI [Conserved Domain Architecture Retrieval Tool (CDART)](https://www.ncbi.nlm.nih.gov/Structure/lexington/docs/cdart_help.html)

taxidlineage.dmp extracted from new_taxdump.zip available in NCBI Taxonomy ftp site (ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/)

## Workflow:
![alt text](https://github.com/NCBI-Codeathons/Taxonomy-specific-RPS-BLAST-part-I/blob/master/Presentation/workflow.png)
Input: a table file generate by a sql querry against CDART database ([example file](https://github.com/NCBI-Codeathons/Taxonomy-specific-RPS-BLAST-part-I/blob/master/src/data/200311.tsv) for PSSM-Id: 200311, pupylate_PafA2)

Output: taxid and/or a taxonomy tree

## Validation:
PSSM-Id: 129695,200311,334026,334050,337780,335786,274086,308214,315456,338615,287328,313550,313551,274263


## FAQ
## People/Team
Marc Gwadz, IEB/NCBI/NIH

Christiam Camacho, IEB/NCBI/NIH

Jianli Dai, IEB/NCBI/NIH

Hanguan Liu, IEB/NCBI/NIH

Mingzhang Yang, IEB/NCBI/NIH

