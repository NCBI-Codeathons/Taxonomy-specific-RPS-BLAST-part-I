#!/usr/bin/env python

from .node import Node

class Tree:
    def __init__(self, root, catalog):
        self.root = root
        self.catalog = catalog

    def search(self, taxid):
        if taxid not in self.catalog:
            return None
        return self.catalog[taxid]

    def trim(self, node):
        pass


def createTree(arr):
    """
    Create a tree using the provided list of tuples. In the tree, a node may contains multiple
    child nodes, but it can only have one parent node.
    :param arr: list of tuples (taxid, weight, lineage), where lineage is a list of taxid
    :return: Tree instance
    """
    root = Node(0, 0)
    catalog = {}
    for bucket in arr:
        leaf = Node(bucket[0], bucket[1])
        iter = root
        for i in range(len(bucket[2])):
            lin = bucket[2][i]
            if catalog.get(lin) is None:
                node = Node(lin, 0)
                iter.addChildNode(node)
                catalog[lin] = node
                iter = node
            else:
                # below we check the compatibility of the data
                # each node can only have one parent node
                eid = catalog[lin].parentNode.taxid
                if i == 0:
                    if eid != root.taxid:
                        m = "node #{} got two parent nodes #{} and #{}".format(lin, eid, root.taxid)
                        raise ValueError(m)
                else:
                    if eid != bucket[2][i-1]:
                        m = "node #{} got two parent nodes #{} and #{}".format(lin, eid, bucket[2][i-1])
                        raise ValueError(m)

                iter = catalog[lin]

        if catalog.get(leaf.taxid) is None:
            iter.addChildNode(leaf)
            catalog[leaf.taxid] = leaf
        else:
            eid = catalog[bucket[0]].parentNode.taxid
            if eid != bucket[2][-1]:
                m = "node #{} got two parent nodes #{} and #{}".format(lin, eid, bucket[2][-1])
                raise ValueError(m)
            iter = catalog[bucket[0]]
            iter.updateWeight(leaf.weight)

    return Tree(root, catalog)

