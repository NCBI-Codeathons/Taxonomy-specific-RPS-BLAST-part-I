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

    def sayGoodbye(self, node):
        # if self.catalog.get(node.taxid) is None:
        #     raise ValueError("node {} not exist in the tree".format(node.taxid))
        self.catalog.pop(node.taxid, None)
        print("node {} removed from the tree".format(node.taxid))

    def trim(self, node):
        if self is None or self.root is None:
            raise ValueError("the tree is empty")
        if self.root.isLeafNode():
            nd = self.root
            self.root = None
            self.catalog = {}
            return nd
        if node is None:
            p = self.root
            while len(p.childNodes) == 1:
                p = p.childNodes[0]

            id_ws = [(c.taxid, c.weight) for c in p.childNodes]
            min_id = sorted(id_ws, key=lambda t : t[1])[0]
            nd = p.removeChildNode(self.catalog[min_id])

            nd.walk(lambda ch : self.sayGoodbye(ch))
            return nd
        else:
            if self.catalog.get(node.taxid) is None:
                raise ValueError("not a child node of this tree")
            elif node.parentNode is None:
                raise ValueError("not a child node of this tree")
            else:
                if node == self.root:
                    node.walk(lambda ch, d, i: self.sayGoodbye(ch))
                    self.root = None
                    return node
                else:
                    node.walk(lambda ch, d, i: self.sayGoodbye(ch))
                    return node.parentNode.removeChildNode(node)

    def __str__(self):
        lines = []
        def func(nd, depth, idx):
            v = 1
            if nd.parentNode is not None and len(nd.parentNode.childNodes) > 1:
                v = len(nd.parentNode.childNodes) - 1

            bs = []
            p = nd
            q = p.parentNode
            while q is not None:
                if len(q.childNodes) > 1 and q.childNodes[-1] != p:
                    bs.append(True)
                else:
                    bs.append(False)
                p = q
                q = p.parentNode
            bs.append(False)
            bs = reversed(bs[1:])
            pre = "".join(["┃   " if b else "    " for b in bs])

            if idx == 0 and len(nd.childNodes) < 2:
                lines.append(pre + "┕━━━" + str(nd.taxid))
            elif idx == v:
                lines.append(pre + "┕━━━" + str(nd.taxid))
            else:
                lines.append(pre + "┝━━━" + str(nd.taxid))


        self.root.walk(func)
        return "\n".join(lines)








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

