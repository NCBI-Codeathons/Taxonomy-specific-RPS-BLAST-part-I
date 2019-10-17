from taxtree.tree import Tree, createTree

tree = createTree([
    (88, 2, [1, 2, 3, 4, 5]),
    (66, 2, [1, 12, 13, 14, 15]),
    (99, 2, [200, 22, 23, 24, 25]),
    (96, 2, [1, 12, 230, 34, 45]),
    (87, 2, [2000, 20, 30, 40, 50]),
])

print(tree.root)