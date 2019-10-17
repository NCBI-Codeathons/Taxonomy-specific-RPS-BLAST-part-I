# Taxonomy-specific-RPS-BLAST-part-I
This 2019 NCBI-Codeathon project will develop a pipeline to assign a taxonomy id to a conserved protein domain (Position-Specific Score Matrix, [PSSM](https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd_help.shtml#CD_PSSM)). The taxonomy id represents the taxon that contains this domain specifically. This taxonomy id will be incorporated into [RPS-Blast](https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd_help.shtml#RPSBWhat) to provide taxonomy information in [CD Search](https://www.ncbi.nlm.nih.gov/Structure/cdd/wrpsb.cgi).

Input: PSSM-Id or PSSM Accession, e.g 200311 or TIGR03687 for pupylate_PafA2

Output: taxid, a taxonomy tree (planning)

## Dependencies:
Python 3.7
[ETE toolkit v3.1.1 or above](http://etetoolkit.org/documentation/ete-ncbiquery/)

## Workflow:
## Validation:

## FAQ
## People/Team
Marc Gwadz, NCBI/NIH
Christiam Camacho, NCBI/NIH
Jianli Dai, NCBI/NIH
Hanguan Liu, NCBI/NIH
Mingzhang Yang, NCBI/NIH
