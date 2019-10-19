$ ./dtrt.py data/129695.tsv
------------------------------------
total number of nodes: 4474
total weight initially: 2722
total weight for now: 2722
total number of leaf nodes: 1575
the deepest node is of depth: 36
------------------------------------

lowest common node:
| TaxId: 131567
| Weight: 2722
| Path: /0/131567
| Child Nodes: [2759, 2, 2157]
| Child Weights: [2424, 294, 4]

potential outlier:
| TaxId: 2157
| Weight: 4
| Path: /0/131567/2157
| Child Nodes: [1783276, 29294, 28890]
| Child Weights: [2, 1, 1]


to meet the threshold 95.00%, the lowest common node is:
| TaxId: 131567
| Weight: 2718
| Path: /0/131567
| Child Nodes: [2759, 2]
| Child Weights: [2424, 294]

the current percentage is 99.85%

-----------------------------------------------------------------------------------------------------------

$ ./dtrt.py data/129695.tsv -shake
------------------------------------
total number of nodes: 4474
total weight initially: 2722
total weight for now: 2722
total number of leaf nodes: 1575
the deepest node is of depth: 36
------------------------------------

after shaking, the tree status is as below:

------------------------------------
total number of nodes: 4142
total weight initially: 2722
total weight for now: 2627
total number of leaf nodes: 1506
the deepest node is of depth: 36
------------------------------------

lowest common node:
| TaxId: 131567
| Weight: 2627
| Path: /0/131567
| Child Nodes: [2759, 2]
| Child Weights: [2336, 291]

potential outlier:
| TaxId: 2
| Weight: 291
| Path: /0/131567/2
| Child Nodes: [57723, 1224, 1783272, 2323, 1783270]
| Child Weights: [12, 125, 115, 16, 23]


to meet the threshold 95.00%, the lowest common node is:
| TaxId: 131567
| Weight: 2627
| Path: /0/131567
| Child Nodes: [2759, 2]
| Child Weights: [2336, 291]

the current percentage is 96.51%