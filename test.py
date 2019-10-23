#!/usr/bin/env python3
from taxtree.tree import Tree, createTree

tree = createTree([
    (88, 2, [1, 2, 3, 4, 5, 6, 7, 8]),
    (66, 8, [1, 12, 13, 14, 15]),
    (99, 4, [200, 22, 23, 24, 25]),
    (96, 2, [1, 12, 230, 34, 45]),
    (87, 1, [2000, 20, 30, 40, 50]),
])

tree._root.show()

print(tree._catalog[40])
print(tree._catalog[40].toJSON())

# print(tree)
# print(tree.nearestAncestor(tree.search(34), tree.search(7)))
# tree.describe()
# tree.report(.6)
# tree.describe()
# print("lowest common node:")
# print(tree.lowestCommonNode())
# print("possible outlier:")
# print(tree.possibleOutlier())

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