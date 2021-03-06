#!/usr/bin/env python3
from taxtree.tree import createTree

tree = createTree([
    (88, 2, [1, 2, 3, 4, 5]),
    (66, 80, [1, 12, 13, 14, 15]),
    (99, 40, [200, 22, 23, 24, 25]),
    (96, 2, [1, 12, 230, 34, 45]),
    (87, 1, [2000, 20, 30, 40, 50]),
])

print(tree)

tree.shake(.2)

print(tree)

print("lowest common node:")
print(tree.lowestCommonNode())
print("possible outlier:")
print(tree.potentialOutlier())

# print(tree.root)

# for i in [1, 200, 2000]:
#     print("----------")
#     tree.trim(tree.catalog[i])
#     print(tree.root)
#
# tree.trim()
# print(tree)
#
# tree.trim()
# print(tree)
#
# tree.trim()
# print(tree)
