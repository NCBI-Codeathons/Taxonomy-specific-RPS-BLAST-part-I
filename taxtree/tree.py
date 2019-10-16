from .node import Node

class Tree:
    def __init__(self, root, catalog):
        self.root = root
        self.catalog = catalog

    def search(self, taxid):
        if taxid not in self.catalog:
            return None
        return self.catalog[taxid]


def createTree(arr):
    """
    Create a tree using the provided list of tuples
    :param arr: list of tuples (taxid, weight, lineage), where lineage is a list of taxid
    :return: Tree instance
    """
    root = Node(0, 0)
    catalog = {}
    for bucket in arr:
        leaf = Node(bucket[0], bucket[1])
        iter = root
        for lin in bucket[2]:
            if catalog[lin] is None:
                node = Node(lin, 0)
                iter.addChildNode(node)
                iter = node
                catalog[lin] = node
            else:
                iter = catalog[lin]

        if catalog[bucket[0]] is None:
            iter.addChildNode(leaf)
        else:
            iter = catalog[bucket[0]]
            iter.mergeNewNode(leaf)

